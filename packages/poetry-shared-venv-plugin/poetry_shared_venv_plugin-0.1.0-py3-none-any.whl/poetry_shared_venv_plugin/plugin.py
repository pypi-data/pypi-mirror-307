import fnmatch
import glob
import pathlib
from typing import Dict, List, Tuple, TypedDict

import cleo.events.console_command_event
import cleo.events.console_events
import cleo.events.event_dispatcher
import cleo.io.inputs
import cleo.io.inputs.argv_input
import cleo.io.inputs.input
import cleo.io.io
import cleo.io.outputs.output
from cleo.io.outputs.output import Verbosity
from poetry.console.application import Application
from poetry.console.commands.add import AddCommand
from poetry.console.commands.install import InstallCommand
from poetry.console.commands.lock import LockCommand
from poetry.console.commands.remove import RemoveCommand
from poetry.console.commands.update import UpdateCommand
from poetry.core.packages.directory_dependency import DirectoryDependency
from poetry.factory import Factory
from poetry.installation.installer import Installer
from poetry.plugins.application_plugin import ApplicationPlugin
from poetry.poetry import Poetry
from poetry.toml import TOMLFile
from poetry.utils.env import Env, EnvManager
from tomlkit import TOMLDocument

defaults_exclude = {
    "**/*.pyc/**/*",
    "**/__pycache__/**/*",
    "**/.venv/**/*",
    "**/.mypy_cache/**/*",
    "**/node_modules/**/*",
    "**/.git/**/*",
    "**/dist/**/*",
}


class PluginConfig(TypedDict):
    enabled: bool
    root: bool
    include: list[str]
    exclude: list[str]


class SharedVenvPlugin(ApplicationPlugin):
    def __init__(self):
        self.poetry = None
        self.application = None
        self.config: PluginConfig = {"enabled": False, "root": False, "include": [], "exclude": defaults_exclude}
        self.io = None

    def activate(self, application: Application):
        application.event_dispatcher.add_listener(cleo.events.console_events.COMMAND, self.event_listener)

        self.poetry = application.poetry
        self.application = application

    def event_listener(
        self,
        event: cleo.events.console_command_event.ConsoleCommandEvent,
        event_name: str,
        dispatcher: cleo.events.event_dispatcher.EventDispatcher,
    ) -> None:
        self.io = event.io
        self.config = self._get_config(self.poetry.pyproject.data)

        if isinstance(event.command, (InstallCommand, LockCommand)) and self.config["enabled"] and self.config["root"]:
            self.load_workspace_dependencies(self.poetry, self.config)

        elif isinstance(event.command, (InstallCommand, LockCommand, AddCommand, UpdateCommand, RemoveCommand)):
            root_pyproject_dir: pathlib.Path = None
            root_pyproject_path: str = None
            root_pyproject: TOMLDocument = None

            for parent in self.poetry.file.path.parents:
                if parent.joinpath("pyproject.toml").exists():
                    pyproject = TOMLFile(parent.joinpath("pyproject.toml")).read()
                    if self._get_config(pyproject)["root"]:
                        root_pyproject_dir = parent
                        root_pyproject_path = parent.joinpath("pyproject.toml")
                        root_pyproject = pyproject
                        break

            if root_pyproject_path:
                original_handle = event.command.handle

                def _wrapper():
                    root_poetry = Factory().create_poetry(root_pyproject_path)
                    self.load_workspace_dependencies(root_poetry, self._get_config(root_pyproject), root_pyproject_dir)

                    root_env = EnvManager(root_poetry, io=event.io).create_venv()
                    event.command.set_env(root_env)
                    event.command.set_installer(
                        Installer(
                            event.command.installer._io,
                            root_env,
                            self.poetry.package,
                            self.poetry.locker,
                            self.poetry.pool,
                            self.poetry.config,
                        )
                    )

                    original_handle()
                    dependee_graph = self.get_dependee_graph(root_poetry)

                    exit_code = self._sync_dependee(
                        event, dependee_graph, root_pyproject_dir, root_env, self.poetry.package.name
                    )
                    if exit_code != 0:
                        return exit_code

                    self._sync_root_pyproject(event, root_poetry, root_env)

                event.command.handle = _wrapper

    def _sync_dependee(
        self,
        event: cleo.events.console_command_event.ConsoleCommandEvent,
        graph: Dict[str, List[Tuple[str, str]]],
        root_dir: pathlib.Path,
        root_env: Env,
        package_name: str,
    ) -> int:
        for dependee_name, dependee_path in graph[package_name]:
            relative_path = pathlib.Path(dependee_path).relative_to(root_dir)
            event.command.line(f"Syncing <c1>{dependee_name} ({relative_path}/poetry.lock)</c1> ")
            dependee_poetry = Factory().create_poetry(pathlib.Path(dependee_path).joinpath("pyproject.toml"))

            lock_command = LockCommand()
            lock_command.set_application(event.command.application)
            lock_command.set_poetry(dependee_poetry)
            lock_command.set_env(root_env)
            lock_command.configure()
            lock_command.set_installer(
                Installer(
                    event.command.installer._io,
                    root_env,
                    dependee_poetry.package,
                    dependee_poetry.locker,
                    dependee_poetry.pool,
                    dependee_poetry.config,
                )
            )
            lock_result = lock_command.run(
                cleo.io.io.IO(
                    input=cleo.io.inputs.argv_input.ArgvInput(argv=["--no-update"]),
                    output=event.io.output,
                    error_output=event.io.error_output,
                )
            )

            if lock_result != 0:
                return lock_result

            return self._sync_dependee(event, graph, root_dir, root_env, dependee_name)

        return 0

    def _sync_root_pyproject(
        self, event: cleo.events.console_command_event.ConsoleCommandEvent, root_poetry: Poetry, root_env: Env
    ):
        event.command.line("Syncing root <c1>pyproject.toml</c1>")
        lock_command = LockCommand()
        lock_command.set_application(event.command.application)
        lock_command.set_poetry(root_poetry)
        lock_command.set_env(root_env)
        lock_command.configure()
        lock_command.set_installer(
            Installer(
                event.command.installer._io,
                root_env,
                root_poetry.package,
                root_poetry.locker,
                root_poetry.pool,
                root_poetry.config,
            )
        )
        lock_result = lock_command.run(
            cleo.io.io.IO(
                input=cleo.io.inputs.argv_input.ArgvInput(argv=["--no-update"]),
                output=event.io.output,
                error_output=event.io.error_output,
            )
        )

        if lock_result != 0:
            return lock_result

        if not isinstance(event.command, LockCommand):
            event.command.line("Installing root dependencies")
            install_command = InstallCommand()
            install_command.set_application(event.command.application)
            install_command.set_poetry(root_poetry)
            install_command.set_env(root_env)
            install_command.configure()
            install_command.set_installer(
                Installer(
                    event.command.installer._io,
                    root_env,
                    root_poetry.package,
                    root_poetry.locker,
                    root_poetry.pool,
                    root_poetry.config,
                )
            )
            return install_command.run(
                cleo.io.io.IO(
                    input=cleo.io.inputs.argv_input.ArgvInput(argv=[]),
                    output=event.io.output,
                    error_output=event.io.error_output,
                )
            )

    def get_dependee_graph(self, poetry: Poetry) -> Dict[str, List[Tuple[str, str]]]:
        main_dependencies = poetry.package.dependency_group("main").dependencies
        graph = {}

        for dependency in main_dependencies:
            if not dependency.is_directory():
                continue

            if dependency.name not in graph:
                graph[dependency.name] = []

            for sub_dependency in main_dependencies:
                if not sub_dependency.is_directory():
                    continue

                if sub_dependency.name == dependency.name:
                    continue

                pyproject_path = pathlib.Path(sub_dependency.source_url).joinpath("pyproject.toml")
                pyproject = TOMLFile(pyproject_path).read()

                if dependency.name in pyproject["tool"]["poetry"].get("dependencies", {}):
                    graph[dependency.name].append((sub_dependency.name, sub_dependency.source_url))

        return graph

    def load_workspace_dependencies(
        self, poetry: Poetry, config: PluginConfig, root_dir: pathlib.Path = pathlib.Path(".")
    ):
        for pattern in config["include"]:
            for path in glob.glob(f"{pattern}/pyproject.toml", root_dir=root_dir, recursive=True):
                if any(fnmatch.fnmatch(path, exclude) for exclude in self.config["exclude"]):
                    continue

                pyproject = TOMLFile(root_dir.joinpath(path)).read()
                package_name = pyproject["tool"]["poetry"]["name"]

                self.io.write_line(f"Adding dependency <c1>{package_name}</c1>", verbosity=Verbosity.DEBUG)

                poetry.package.add_dependency(
                    DirectoryDependency(
                        name=package_name,
                        path=pathlib.Path(path).parent,
                        base=root_dir,
                        develop=True,
                    )
                )

    def _get_config(self, pyproject: TOMLDocument) -> PluginConfig:
        return {**self.config, **pyproject["tool"].get("shared-venv", {})}
