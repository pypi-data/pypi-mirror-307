import os
import re
from metaflow import current
from metaflow.decorators import StepDecorator
from metaflow.exception import MetaflowException
from metaflow.cards import Markdown, ProgressBar
from metaflow.plugins.cards.card_decorator import CardDecorator
from metaflow.decorators import _attach_decorators_to_step

from .dbt_executor import DBTExecutor, DBTProjectConfig
from ..cards.dbt_docs import DBTDocs


class CommandNotSupported(MetaflowException):
    headline = "DBT command not supported"


class MissingProfiles(MetaflowException):
    headline = "Missing DBT Profiles configuration"


class MissingStateStorage(MetaflowException):
    headline = "Missing DBT State Storage configuration"


class MissingMacroName(MetaflowException):
    headline = "Missing macro name for run-operation"


class DbtStepDecorator(StepDecorator):
    """
    Decorator to execute DBT models before a step execution begins.


    Parameters
    ----------
    command: str, optional. Default 'run'
        DBT command to execute. Default is 'run'.
        Supported commands are: run, seed, test, build and run-operation
    macro : str, optional
        name for macro to run. Required with the 'run-operation' command
    args : str, optional
        args to pass for macro. Only used with the 'run-operation' commmand.
    project_dir: str, optional
        Path to the DBT project that contains a 'dbt_project.yml'.
        If not specified, the current folder and parent folders will be tried.
    models: List[str], optional
        List of model name(s) to run. All models will be run by default if no model name is provided.
    select: List[str], optional
        List of object name(s) to run.
    exclude: List[str], optional
        List of model name(s) to exclude. Nothing is excluded by default.
    target: str, optional
        Chooses which target to load from the profiles.yml file.
        If not specified, it will use the default target from the profiles.
    profiles: Dict[str, Union[str, Dict]]
        a configuration dictionary that will be translated into a valid profiles.yml for the dbt CLI.
    """

    name = "_dbt"

    defaults = {
        "command": "run",
        "macro": None,
        "args": None,
        "project_dir": None,
        "models": None,
        "select": None,
        "exclude": None,
        "target": None,
        "profiles": None,
        "generate_docs": False,  # TODO: This could also be true by default
        #  TODO: Add way to specify adapter through decorator as well.
    }

    def __init__(self, attributes=None, statically_defined=False):
        super(DbtStepDecorator, self).__init__(attributes, statically_defined)

    def step_init(
        self, flow, graph, step_name, decorators, environment, flow_datastore, logger
    ):
        if self.attributes["profiles"] is None and not os.path.exists("./profiles.yml"):
            raise MissingProfiles(
                "You must provide profiles configuration for the DBT decorator.\n"
                "Either provide a dictionary for the 'profiles=' attribute "
                "or create a 'profiles.yml' file in the flow folder."
            )

        cmd = self.attributes["command"]

        if cmd not in ["run", "seed", "test", "build", "run-operation"]:
            raise CommandNotSupported(f"command '{cmd}' is not supported.")

        if cmd == "run-operation" and self.attributes["macro"] is None:
            raise MissingMacroName(
                "Specify the macro name to run with the 'macro=' option on the DBT decorator for the *%s* step."
                % step_name
            )

        # Do we need persisted state due to the selectors or not?
        self.use_state = self.attributes["models"] and any(
            any(sel in val for val in self.attributes["models"])
            for sel in ["result:", "state:"]
        )

        self.ds_type = flow_datastore.TYPE

    def task_pre_step(
        self,
        step_name,
        task_datastore,
        metadata,
        run_id,
        task_id,
        flow,
        graph,
        retry_count,
        max_user_code_retries,
        ubf_context,
        inputs,
    ):
        self.run_id = run_id
        self.step_name = step_name

    def task_decorate(
        self, step_func, flow, graph, retry_count, max_user_code_retries, ubf_context
    ):
        # We want to use a run and task independent prefix for the state store,
        # so that consecutive executions have a known location to look in for previous state
        # TODO: cover projects.
        # TODO: evaluate prefix for sufficient uniqueness
        state_prefix = f"{flow.name}/{step_func.__name__}"
        build_cache_prefix = f"{flow.name}/{self.run_id}"
        with DBTExecutor(
            models=self.attributes["models"],
            macro=self.attributes["macro"],
            args=self.attributes["args"],
            select=self.attributes["select"],
            exclude=self.attributes["exclude"],
            project_dir=self.attributes["project_dir"],
            target=self.attributes["target"],
            profiles=self.attributes["profiles"],
            state_prefix=state_prefix if self.use_state else None,
            build_cache_prefix=build_cache_prefix,
            ds_type=self.ds_type,
        ) as executor:
            # execute the command

            cmd_exception = None
            try:
                for output in executor.command(self.attributes["command"]):
                    print(output, end="")
                    self._parse_result_card(output)
            except Exception as ex:
                # we do not want to immediately fail in case of a failing DBT command,
                # as we still want to try and persist artifacts etc.
                cmd_exception = ex

            if self.attributes["generate_docs"]:
                try:
                    # This might fail due to DBT version not supporting docs creation.
                    # We don't want to fail outright due to docs alone
                    out = ""
                    for line in executor.command("docs"):
                        out += line
                except Exception:
                    print(out)
                    pass

            # Write DBT run artifacts as task artifacts.
            # TODO: don't hardcode artifacts if at all not necessary.
            def _dbt_artifacts_iterable():
                artifacts = {
                    "run_results": executor.run_results,
                    "semantic_manifest": executor.semantic_manifest,
                    "manifest": executor.manifest,
                    "sources": executor.sources,
                    "catalog": executor.catalog,
                    "static_index": executor.static_index,
                }
                for name, func in artifacts.items():
                    val = func()
                    if val is None:
                        continue
                    yield (name, val)

            for k, v in _dbt_artifacts_iterable():
                setattr(flow, k, v)

            # update possible errors to the results card
            self._add_errors(executor.run_results())

            if cmd_exception:
                # finally raise if an error was encountered with the DBT command earlier.
                raise cmd_exception

        return step_func

    def _parse_result_card(self, output):
        # Init card if missing
        if not getattr(self, "result_card", None):
            self.result_card = current.card["dbt_results"]

        if not getattr(self, "result_header", None):
            self.result_header = Markdown("# Running DBT Command")
            self.result_card.append(self.result_header)

        if not getattr(self, "result_progress", None):
            self.result_progress = None
        # DBT logs progress in stdout with 'x of y' pattern for steps, so we rely on this for parsing.
        # example:
        # 1 of 50 START
        # 1 of 50 OK
        progress_info_regex = re.compile(r".* (\d+) of (\d+) OK.*")

        matched = progress_info_regex.match(output)
        if matched:
            cur, total = matched.group(1, 2)
            if not self.result_progress:
                self.result_progress = ProgressBar(max=total, label="Parts done")
                self.result_card.append(self.result_progress)

            self.result_progress.update(cur)
            self.result_card.refresh()

    def _add_errors(self, run_results=None):
        if not run_results:
            return
        # Init card if missing
        if not getattr(self, "result_card", None):
            self.result_card = current.card["dbt_results"]

        failures = [
            result for result in run_results["results"] if result["status"] != "success"
        ]
        for failure in failures:
            failure_comp = [
                Markdown("# Error with: %s" % failure["unique_id"]),
                Markdown(failure["message"]),
            ]
            self.result_card.extend(failure_comp)

        self.result_card.refresh()

    def add_to_package(self):
        """
        Called to add custom packages needed for a decorator. This hook will be
        called in the `MetaflowPackage` class where metaflow compiles the code package
        tarball. This hook is invoked in the `MetaflowPackage`'s `path_tuples`
        function. The `path_tuples` function is a generator that yields a tuple of
        `(file_path, arcname)`.`file_path` is the path of the file in the local file system;
        the `arcname` is the path of the file in the constructed tarball or the path of the file
        after decompressing the tarball.

        Returns a list of tuples where each tuple represents (file_path, arcname)
        """
        config = DBTProjectConfig(self.attributes["project_dir"])
        paths = config.project_file_paths()

        # TODO: verify keys for possible collisions.
        files = [(path, path) for path in paths]
        return files
