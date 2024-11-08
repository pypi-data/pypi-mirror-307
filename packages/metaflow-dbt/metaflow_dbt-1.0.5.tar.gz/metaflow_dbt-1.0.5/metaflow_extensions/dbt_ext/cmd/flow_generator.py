from copy import deepcopy
from itertools import chain
from typing import List

PARSE_TYPES = ("raw", "leaves")


class AdditionalDeco:
    def __init__(self, name, attr: List[str] = [], constant: str = None) -> None:
        self.name = name
        self.attr = attr
        self.constant = constant

    @property
    def decospec(self):
        return f"@{self.name}({self.attr})" if self.attr else f"@{self.name}"


class FlowGenerator:
    def __init__(
        self,
        manifest,
        flow_name,
        project_dir,
        flow_decorators: List[AdditionalDeco] = [],
        step_decorators: List[AdditionalDeco] = [],
        parse_type="raw",
    ):
        self.name = flow_name
        self.manifest = manifest
        self.flow_str = None
        self.parse_type = parse_type
        self.extra_constants = [
            deco.constant
            for deco in (flow_decorators + step_decorators)
            if deco.constant is not None
        ]
        self.extra_flow_decorators = [deco.decospec for deco in flow_decorators]
        self.extra_step_decorators = [deco.decospec for deco in step_decorators]
        self.extra_imports = [deco.name for deco in (flow_decorators + step_decorators)]
        # we're not interested in the default case, as we do not need to specify this in the decorator
        # attributes.
        self.project_dir = project_dir if not project_dir == "./" else None

    def generate(self):
        # crawl through
        # - manifest['child_map'] : lists children of a node
        # - manifest['parent_map'] : lists dependencies for a node
        # to form a graph for the Flow
        child_map = deepcopy(self.manifest["child_map"])
        parent_map = deepcopy(self.manifest["parent_map"])

        # Sort the nodes based on dependencies
        def _visit(nodes: set, sorted: List):
            if not nodes:
                return sorted
            _nodes = set(nodes)
            for node in nodes:
                if not parent_map[node]:
                    sorted.append(node)
                    _nodes.remove(node)
                    for child in child_map[node]:
                        parent_map[child].remove(node)
            return _visit(_nodes, sorted)

        sorted_nodes = _visit(set(child_map.keys()), [])

        supported_sorted_nodes = list(
            filter(
                lambda node: node.startswith("model") or node.startswith("seed"),
                sorted_nodes,
            )
        )
        parsers = {"raw": self.raw_parsing, "leaves": self.leaf_parsing}

        node_objs = parsers[self.parse_type](supported_sorted_nodes)

        self.flow_str = self.flow_template(node_objs)

    def raw_parsing(self, sorted_nodes):
        # Use the list of sorted nodes to construct steps
        node_objs = []
        for i, node in enumerate(sorted_nodes):
            next_node = sorted_nodes[i + 1] if i < len(sorted_nodes) - 1 else None
            cmd = node.split(".", 1)[0]
            cmd = None if cmd == "model" else cmd
            node_objs.append(
                DBTNode(
                    self.manifest["nodes"][node]["name"],
                    self.manifest["nodes"][next_node]["name"] if next_node else None,
                    cmd,
                    self.project_dir is not None,
                    self.extra_step_decorators,
                )
            )
        return node_objs

    def leaf_parsing(self, sorted_nodes):
        # filter leaves from nodes
        parent_map = self.manifest["parent_map"]
        child_map = self.manifest["child_map"]
        leaves = []
        for node in sorted_nodes:
            true_children = [n for n in child_map[node] if not n.startswith("test.")]
            if not true_children and parent_map[node]:
                leaves.append(node)

        # Seeds need to be run separately.
        seeds_and_leaves = [
            n for n in sorted_nodes if n.startswith("seed.") or n in leaves
        ]

        def _gather(node):
            # gather dependencies for a node recursively.
            deps = []
            parents = [
                p
                for p in parent_map[node]
                if p.startswith("seed.") or p.startswith("model.")
            ]
            if parents:
                deps.extend(parents)
                for parent in parents:
                    deps.extend(_gather(parent))
            return deps

        # construct tree with branches
        tree = []
        tail = [
            n for n in sorted_nodes if n.startswith("seed.") or n.startswith("model.")
        ]
        for n in seeds_and_leaves:
            branch = [n for n in [n] + _gather(n)]
            tree.append([n for n in sorted_nodes if n in branch])
            tail = [n for n in tail if n not in branch]

        # add tail branch if one exists
        tree.append([n for n in sorted_nodes if n in tail])

        def shared_ancestors_set(branches=[]):
            # return a set of nodes that are shared by at least one branch (and need to therefore be deduplicated)
            common_ancestors = set()
            for branch in branches:
                for n in branch:
                    if (
                        n not in common_ancestors
                        and len([n for b in branches if n in b]) > 1
                    ):
                        common_ancestors.add(n)

            return common_ancestors

        def partition(branch):
            # partition a branch into subsets of similar type of nodes, up to a maximum number of nodes
            ntype = None
            part = []
            maxnodes = 10
            sorted_partitions = []
            for n in branch:
                nt, _ = n.split(".", 1)
                if ntype is None:
                    ntype = nt
                if nt != ntype:
                    # save current collected nodes
                    sorted_partitions.append(part)
                    ntype = nt
                    # start a new partition
                    part = [n]
                else:
                    part.append(n)
            # append last part outside of the iteration
            sorted_partitions.append(part)

            return sorted_partitions

        def parse_tree(branches):
            ancestry = shared_ancestors_set(branches)
            sorted_ancestry = [n for n in sorted_nodes if n in ancestry]
            trimmed_branches = [[n for n in b if n not in ancestry] for b in branches]
            # remove empty branches
            trimmed_branches = [branch for branch in trimmed_branches if branch]

            return sorted_ancestry, trimmed_branches

        ancestors, branches = parse_tree(tree)

        # Use the list of sorted nodes to construct steps
        node_objs = []

        branch_entry_fns = []
        for branch in branches:
            branch_name_stub = self.get_node_name(branch[-1])
            pt = partition(branch)
            for idx, part in enumerate(pt):
                name = "dbt_%s_%d" % (branch_name_stub, idx)
                if idx == 0:
                    branch_entry_fns.append(name)
                nextname = (
                    "dbt_%s_%d" % (branch_name_stub, idx + 1)
                    if idx < len(pt) - 1
                    else "join_dbt_branches"
                )
                cmd = get_node_cmd(part[0])
                node_objs.append(
                    DBTMultiNode(
                        name,
                        [nextname],
                        cmd,
                        self.project_dir is not None,
                        self.extra_step_decorators,
                        [self.get_node_name(n) for n in part],
                    )
                )
        node_objs.append(JOIN_NODE)

        ancestor_nodes = []
        ancestor_parts = partition(ancestors)
        for idx, part in enumerate(ancestor_parts):
            name = "dbt_shared_parents_%d" % idx
            nextnames = (
                ["dbt_shared_parents_%d" % (idx + 1)]
                if idx < len(ancestor_parts) - 1
                else branch_entry_fns
            )
            cmd = get_node_cmd(part[0])
            ancestor_nodes.append(
                DBTMultiNode(
                    name,
                    nextnames,
                    cmd,
                    self.project_dir is not None,
                    self.extra_step_decorators,
                    [self.get_node_name(n) for n in part],
                )
            )

        return ancestor_nodes + node_objs

    def get_node_name(self, node):
        return self.manifest["nodes"][node]["name"]

    def write(self):
        if not self.flow_str:
            raise Exception("Flow not generated, nothing to write yet.")
        filename = str(self.name).lower() + ".py"
        with open(filename, "w") as f:
            f.write(self.flow_str)

        return filename

    def flow_template(self, dbt_nodes: List):
        first_node_name = dbt_nodes[0].name
        constants = "".join(
            const
            for const in [
                f'PROJECT_DIR="{self.project_dir}"' if self.project_dir else None,
            ]
            + [
                f"""
{const}"""
                for const in self.extra_constants
            ]
            if const is not None
        )
        metaflow_imports = ", ".join(
            [
                dep
                for dep in [
                    "step",
                    "FlowSpec",
                    "dbt",
                ]
                if dep is not None
            ]
            + self.extra_imports
        )

        flow_decos = "".join(
            f"""
{deco}"""
            for deco in self.extra_flow_decorators
        )
        template = f"""
from metaflow import {metaflow_imports}

{constants}
{flow_decos}
class {self.name}(FlowSpec):
    
    @step
    def start(self):
        print("Starting the generated DBT Flow")
        self.next(self.{sanitize(first_node_name)})"""
        for node in dbt_nodes:
            template += str(node)

        template += f"""
    @step
    def end(self):
        print("DBT executed successfully")

if __name__=="__main__":
    {self.name}()
"""

        return template


class DBTNode:
    def __init__(
        self,
        node_name: str,
        next_node_name: str = None,
        command: str = None,
        project_dir=False,
        extra_step_decorators=[],
        include_parents=False,
    ):
        # necessary as model names might start with a number, but python functions cannot.
        func_prefix = "dbt_"
        self.name = func_prefix + node_name
        self.next_node_name = (
            (func_prefix + next_node_name) if next_node_name else "end"
        )
        include_op = "+" if include_parents else ""
        self.cmd_str = command if command else "run"
        deco_attrs = ", ".join(
            attr
            for attr in [
                f'command="{command}"' if command else None,
                f'models=["{include_op}{node_name}"]',
                "project_dir=PROJECT_DIR" if project_dir else None,
            ]
            if attr is not None
        )
        self.deco_stack = "".join(
            deco
            for deco in [
                f"""
    @dbt({deco_attrs})""",
            ]
            + [
                f"""
    {deco}"""
                for deco in extra_step_decorators
            ]
            if deco is not None
        )

    def __str__(self) -> str:
        return f"""
    {self.deco_stack}
    @step
    def {sanitize(self.name)}(self):
        self.next(self.{sanitize(self.next_node_name)})
"""


class DBTMultiNode:
    def __init__(
        self,
        func_name: str,
        next_funcs: List[str] = None,
        command: str = None,
        project_dir=False,
        extra_step_decorators=[],
        models=[],
    ):
        self.func_name = func_name
        self.name = func_name

        self.next_func_str = ", ".join(f"self.{sanitize(fn)}" for fn in next_funcs)
        self.cmd_str = command if command else "run"
        model_list = ", ".join(f'"{name}"' for name in models)
        deco_attrs = ", ".join(
            attr
            for attr in [
                f'command="{command}"' if command else None,
                f"models=[{model_list}]",
                "project_dir=PROJECT_DIR" if project_dir else None,
            ]
            if attr is not None
        )
        self.deco_stack = "".join(
            deco
            for deco in [
                f"""
    @dbt({deco_attrs})""",
            ]
            + [
                f"""
    {deco}"""
                for deco in extra_step_decorators
            ]
            if deco is not None
        )

    def __str__(self) -> str:
        return f"""
    {self.deco_stack}
    @step
    def {sanitize(self.func_name)}(self):
        self.next({self.next_func_str})
"""


JOIN_NODE = """
    @step
    def join_dbt_branches(self, inputs):
        self.next(self.end)
"""


def sanitize(name: str):
    return name.replace(".", "_")


def get_node_cmd(node):
    return "seed" if node.startswith("seed.") else None
