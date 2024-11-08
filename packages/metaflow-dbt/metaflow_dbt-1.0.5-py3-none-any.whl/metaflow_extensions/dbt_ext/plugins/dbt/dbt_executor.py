import subprocess
import os
import tempfile
import json
import yaml
import glob
import shutil
from typing import Dict, List, Optional
import tarfile

from metaflow.exception import MetaflowException
from metaflow.util import which
from metaflow.plugins.datatools.s3 import S3
from metaflow.metaflow_config import DEBUG_DBT


class DBTExecutionFailed(MetaflowException):
    headline = "DBT Run execution failed"


class UnsupportedCommand(MetaflowException):
    headline = "Command is not supported"


class DBTDuplicateDependencyFile(MetaflowException):
    headline = "Duplicate dependency file found"


PRECOMPILE_METAFILE = ".precompile.done"
STATE_PUSH_METAFILE = ".state-push.done"
STATE_PULL_METAFILE = ".state-pull.done"


def debug_log(line: str):
    if not DEBUG_DBT:
        return
    print(line)


# TODO: There is a choice to utilize the Python library provided by DBT for performing the run, and accessing run results as well.
# This would introduce a heavy dependency for the decorator use case, which can be completely avoided with the custom implementation
# via calling the CLI via subprocess only at the point when execution needs to happen. Decide on the approach after PoC is complete.
class DBTExecutor:
    def __init__(
        self,
        models: List[str] = None,
        macro: str = None,
        args: str = None,
        select: List[str] = None,
        exclude: List[str] = None,
        project_dir: str = None,
        target: str = None,
        profiles: Dict = None,
        state_prefix: str = None,
        build_cache_prefix: str = None,
        ds_type=None,
    ):

        self.models = " ".join(models) if models is not None else None
        self.select = " ".join(select) if select is not None else None
        self.exclude = " ".join(exclude) if exclude is not None else None
        self.macro = macro
        self.args = args
        self.project_dir = project_dir
        self.target = target
        self.bin = which("./dbt") or which("dbt")
        if self.bin is None:
            raise DBTExecutionFailed("Can not find DBT binary. Please install DBT")
        self.profiles = profiles
        conf = DBTProjectConfig(project_dir)
        self._project_config = conf.project_config

        _ = (
            conf.project_file_paths()
        )  # trigger setting the dbt_dependencies member variable
        self._dbt_dependencies = conf.dbt_dependencies

        self.state_store = None
        if state_prefix:
            self.state_store = self._init_datastore(ds_type, state_prefix)
        self.build_cache = None
        if build_cache_prefix:
            # we want to add the dbt project name to the cache prefix to avoid collisions,
            # as a flow run can be executing multiple dbt projects
            project_name = self._project_config.get("name", None)
            prefix = (
                "%s/%s" % (build_cache_prefix, project_name)
                if project_name
                else build_cache_prefix
            )
            self.build_cache = self._init_datastore(ds_type, prefix)
        self.tempdir = None
        self.in_context = False

    @staticmethod
    def _init_datastore(ds_type, prefix: str = ""):
        from metaflow.plugins import DATASTORES

        datastore = [d for d in DATASTORES if d.TYPE == ds_type][0]

        root = datastore.get_datastore_root_from_config(print)
        return datastore(f"{root}/dbt_state/{prefix}")

    def run_results(self) -> Optional[Dict]:
        return self._read_dbt_artifact("run_results.json")

    def semantic_manifest(self) -> Optional[Dict]:
        return self._read_dbt_artifact("semantic_manifest.json")

    def manifest(self) -> Optional[Dict]:
        return self._read_dbt_artifact("manifest.json")

    def catalog(self) -> Optional[Dict]:
        return self._read_dbt_artifact("catalog.json")

    def sources(self) -> Optional[Dict]:
        return self._read_dbt_artifact("sources.json")

    def static_index(self) -> Optional[Dict]:
        return self._read_dbt_artifact("static_index.html", raw=True)

    def command(self, cmd: str):
        supported = {
            "run": self.run,
            "parse": self.parse,
            "seed": self.seed,
            "build": self.build,
            "test": self.test,
            "run-operation": self.run_operation,
            "docs": self.generate_docs,
        }
        if cmd not in supported:
            raise UnsupportedCommand(
                'The command "%s" is not supported by the DBT Extension' % cmd
            )

        return supported[cmd]()

    def run(self) -> str:
        args = ["--fail-fast", "--no-use-colors"]
        if self.project_dir is not None:
            args.extend(["--project-dir", self.project_dir])
        if self.models is not None:
            args.extend(["--models", self.models])
        if self.select is not None:
            args.extend(["--select", self.select])
        if self.exclude is not None:
            args.extend(["--exclude", self.exclude])
        if self.target is not None:
            args.extend(["--target", self.target])

        return self._call("run", args)

    def test(self) -> str:
        args = ["--fail-fast", "--no-use-colors"]
        if self.project_dir is not None:
            args.extend(["--project-dir", self.project_dir])
        if self.models is not None:
            args.extend(["--models", self.models])
        if self.select is not None:
            args.extend(["--select", self.select])
        if self.target is not None:
            args.extend(["--target", self.target])

        return self._call("test", args)

    def build(self) -> str:
        args = ["--fail-fast", "--no-use-colors"]
        if self.project_dir is not None:
            args.extend(["--project-dir", self.project_dir])
        if self.models is not None:
            args.extend(["--models", self.models])
        if self.select is not None:
            args.extend(["--select", self.select])
        if self.target is not None:
            args.extend(["--target", self.target])

        return self._call("build", args)

    def run_operation(self) -> str:
        if self.macro is None:
            raise DBTExecutionFailed(
                "run-operation requires specifying the name of a macro to be executed."
            )
        args = [self.macro, "--fail-fast", "--no-use-colors"]
        if self.args is not None:
            args.extend(["--args", self.args])
        if self.project_dir is not None:
            args.extend(["--project-dir", self.project_dir])
        if self.target is not None:
            args.extend(["--target", self.target])

        return self._call("run-operation", args)

    def parse(self) -> str:
        args = ["--fail-fast", "--no-use-colors"]
        if self.project_dir is not None:
            args.extend(["--project-dir", self.project_dir])
        if self.models is not None:
            args.extend(["--models", self.models])
        if self.select is not None:
            args.extend(["--select", self.select])
        if self.exclude is not None:
            args.extend(["--exclude", self.exclude])

        return self._call("parse", args)

    def seed(self) -> str:
        args = ["--no-use-colors"]
        if self.project_dir is not None:
            args.extend(["--project-dir", self.project_dir])
        if self.models is not None:
            args.extend(["--models", self.models])
        if self.select is not None:
            args.extend(["--select", self.select])
        if self.exclude is not None:
            args.extend(["--exclude", self.exclude])
        if self.target is not None:
            args.extend(["--target", self.target])

        return self._call("seed", args)

    def generate_docs(self) -> str:
        # The static docs generation requires dbt-core >= 1.7
        args = ["generate", "--static", "--no-compile", "--no-use-colors"]
        if self.project_dir is not None:
            args.extend(["--project-dir", self.project_dir])
        if self.models is not None:
            args.extend(["--models", self.models])
        if self.select is not None:
            args.extend(["--select", self.select])
        if self.exclude is not None:
            args.extend(["--exclude", self.exclude])
        if self.target is not None:
            args.extend(["--target", self.target])

        return self._call("docs", args)

    def _read_dbt_artifact(self, name: str, raw: bool = False):
        artifact = os.path.join(
            ".",
            self.project_dir or "",
            self._project_config.get("target-path", "target"),
            name,
        )
        try:
            with open(artifact) as m:
                return m.read() if raw else json.load(m)
        except FileNotFoundError:
            return None

    def _push_state(self):
        # Push new state to self.state_store if configured
        if not self.state_store:
            return
        target_path = os.path.join(
            ".",
            self.project_dir or "",
            self._project_config.get("target-path", "target"),
        )
        marker = os.path.join(target_path, STATE_PUSH_METAFILE)
        if os.path.exists(marker):
            debug_log("Skipped: State assets have already been pushed once.")
            return

        files_and_paths = {
            key: os.path.join(
                target_path,
                key,
            )
            for key in ["manifest.json", "run_results.json"]
        }
        files_and_handles = {
            key: open(path, mode="rb")
            for key, path in files_and_paths.items()
            if os.path.exists(path)
        }

        self.state_store.save_bytes(
            (name, content) for name, content in files_and_handles.items()
        )

        # write a marker that state has been pushed once.
        with open(marker, "w") as f:
            f.write("")

    def _pull_state(self):
        # Fetch previous state to tempdir from self.state_store if configured
        if not self.state_store:
            return None
        state_path = os.path.join(self.tempdir, "prev_state")
        os.makedirs(state_path, exist_ok=True)

        marker = os.path.join(state_path, STATE_PULL_METAFILE)
        if os.path.exists(marker):
            debug_log("Skipped: State assets have already been fetched")
            return state_path

        with self.state_store.load_bytes(
            ["manifest.json", "run_results.json"]
        ) as result:
            for key, file, _ in result:
                if file is not None:
                    shutil.move(file, os.path.join(state_path, key))

        # write a marker that state has been pulled once.
        if os.listdir(state_path):
            with open(marker, "w") as f:
                f.write("")
            return state_path
        return None

    def _pull_prebuild(self):
        if not self.build_cache:
            return
        target_path = os.path.join(
            ".",
            self.project_dir or "",
            self._project_config.get("target-path", "target"),
        )

        marker = os.path.join(target_path, PRECOMPILE_METAFILE)
        if os.path.exists(marker):
            debug_log("Skipped: Prebuild assets have already been fetched")
            return
        with self.build_cache.load_bytes(["prebuild_tar"]) as result:
            for key, file, _ in result:
                if file is None:
                    debug_log("Failed to pull prebuild assets, prebuild_tar is missing")
                    return
                with tarfile.open(file, "r:gz") as t:
                    t.extractall()
                    debug_log("Extracted contents of %s to %s " % (file, target_path))

        # Add marker that prebuild assets have been fetched
        # target_path might not exist if we did not get anything to extract from the cache.
        os.makedirs(target_path, exist_ok=True)
        with open(marker, "w") as f:
            f.write("")

    def _push_prebuild(self):
        if not self.build_cache:
            return

        target_path = os.path.join(
            ".",
            self.project_dir or "",
            self._project_config.get("target-path", "target"),
        )
        if not os.path.exists(target_path):
            return

        marker = os.path.join(target_path, PRECOMPILE_METAFILE)
        if os.path.exists(marker):
            debug_log("Skipped: Prebuild assets have already been pushed once.")
            return

        temp_tar = os.path.join(self.tempdir, "prebuild_tar")
        with tarfile.open(temp_tar, "w:gz") as t:
            t.add(target_path)
            debug_log(
                "Added assets from path %s to precompiled assets archive" % target_path
            )

        with open(temp_tar, "rb") as f:
            self.build_cache.save_bytes([("prebuild_tar", f)])
            debug_log("Persisting precompiled assets tar from %s" % temp_tar)

        # Add marker that prebuild assets have been pushed
        with open(marker, "w") as f:
            f.write("")

    def __enter__(self):
        self.tempdir_handle = tempfile.TemporaryDirectory()
        self.tempdir = self.tempdir_handle.__enter__()
        self.in_context = True
        return self

    def __exit__(self, exc, value, tb):
        self.tempdir_handle.__exit__(exc, value, tb)
        self.tempdir = None
        self.in_context = False
        return

    def persist_temp_profiles(self):
        "Write a profiles.yml to the tempdir if necessary. Returns a bool for whether a temp profile exists."
        if self.profiles is None:
            return False
        profiles_path = os.path.join(self.tempdir, "profiles.yml")
        if not os.path.exists(profiles_path):
            # Synthesize a profiles.yml from the passed in config dictionary.
            with open(profiles_path, "w") as f:
                conf = yaml.dump(self.profiles)
                f.write(conf)
                debug_log("Wrote a temporary profile to: %s" % profiles_path)
        return True

    def _call(self, cmd, args):
        if not self.in_context:
            raise Exception("DBT Command need to be called within a context manager")
        profile_args = (
            ["--profiles-dir", self.tempdir] if self.persist_temp_profiles() else []
        )

        state_args = []
        # Try using DBT state
        state_path = self._pull_state()
        if state_path:
            debug_log(f"got state assets!")
            # a previous state was available.
            state_args = ["--state", state_path]
        else:
            # we do not have a previous state,
            # so we need to clean up any known state selectors from args in order to avoid errors.
            def _cleanup(arg: str):
                split = arg.split(",")
                args = [a for a in split if not "state:" in a and not "result:" in a]
                if len(args) < len(split):
                    debug_log(
                        "cleaned up a state selector because no previous state was found."
                    )
                return ",".join(args)

            args = [_cleanup(arg) for arg in args]

        # Pull prebuild assets before DBT Command
        self._pull_prebuild()

        # Install dbt dependencies if the packages.yml or dependenices.yml is provided in the project directory.
        if (
            self._dbt_dependencies
        ):  # Assume there is no dbt_packages directory yet, and install dependencies on the fly.
            process = subprocess.Popen(
                [self.bin, "deps", "--project-dir", self.project_dir],
                stdout=subprocess.PIPE,
            )
            while True:
                process.poll()
                if process.returncode is None:
                    # process is still running
                    line = process.stdout.readline()
                    if not line:
                        # end of stdout, but process has not ended yet.
                        continue
                    yield line.decode()
                elif process.returncode == 0:
                    break
                elif process.returncode != 0:
                    raise DBTExecutionFailed(
                        "Ran into an issue with dbt command: dbt deps."
                    )

        try:
            process = subprocess.Popen(
                [self.bin, cmd] + args + profile_args + state_args,
                stdout=subprocess.PIPE,
            )
            while True:
                process.poll()
                if process.returncode is None:
                    # process is still running
                    line = process.stdout.readline()
                    if not line:
                        # end of stdout, but process has not ended yet.
                        continue
                    yield line.decode()
                elif process.returncode == 0:
                    break
                elif process.returncode != 0:
                    # TODO: would be a nice addition if stdout and stderr were separated here.
                    raise DBTExecutionFailed(
                        "ran into an issue with dbt command: %s" % cmd
                    )
        finally:
            # Push state artifacts to self.state_store
            self._push_state()
            self._push_prebuild()


# We want a separate construct for the project config, so this can be parsed without requiring the dbt binary to be present on the system.
# This way users deploying to remote execution do not need to install DBT on their own machine.
class DBTProjectConfig:
    def __init__(self, project_dir: str = None):
        self.project_dir = project_dir

    @property
    def project_config(self):
        config_path = os.path.join(self.project_dir or "./", "dbt_project.yml")

        try:
            with open(config_path) as f:
                return yaml.load(f, Loader=yaml.Loader)
        except FileNotFoundError:
            raise MetaflowException("No configuration file 'dbt_project.yml' found")

    def project_file_paths(self):
        """
        Return a list of files required for the DBT project.
        Used to include necessary files in the codepackage
        """
        files = []
        _inc = [
            f
            for f in [
                "./profiles.yml",
                os.path.join(self.project_dir or "", "dbt_project.yml"),
            ]
            if os.path.exists(f)
        ]
        files.extend(_inc)

        for component in [
            "model-paths",
            "seed-paths",
            "test-paths",
            "analysis-paths",
            "macro-paths",
        ]:
            rel_path = self.project_config.get(component, [None])[
                0
            ]  # dbt profile config defines the file path inside a List.
            if rel_path is None:
                continue
            component_path = os.path.join(self.project_dir or "", rel_path)
            if not os.path.exists(component_path):
                continue
            for path in glob.glob(os.path.join(component_path, "**"), recursive=True):
                files.append(path)

        # Handle dbt packages
        # Mode 1: user has run dbt deps locally, producing the dbt_packages directory.
        # Mode 1 is for the local execution case, where the user has dbt installed locally and wants to minimize edit distance between local and remote execution.
        dbt_packages = os.path.join(self.project_dir or "", "dbt_packages")
        self.dbt_dependencies = []
        if os.path.exists(dbt_packages):
            for path in glob.glob(os.path.join(dbt_packages, "**"), recursive=True):
                files.append(path)
        # Mode 2: user has a packages.yml or dependencies.yml, include this in the codepackage to run dbt deps on the fly.
        # Mode 2 is for the remote execution case, where the user need not have dbt installed locally.
        else:
            found_files = []
            for file in ["packages.yml", "dependencies.yml"]:
                file_path = os.path.join(self.project_dir or "", file)
                if os.path.exists(file_path):
                    found_files.append(file_path)
            if len(found_files) > 1:
                raise DBTDuplicateDependencyFile(
                    "Found 'packages.yml' and 'dependencies.yml' in the dbt project directory: %s. Choose one. Read more at %s."
                    % (found_files, "https://docs.getdbt.com/docs/build/packages")
                )
            if found_files:
                self.dbt_dependencies = found_files[0]
                files.append(found_files[0])

        return files
