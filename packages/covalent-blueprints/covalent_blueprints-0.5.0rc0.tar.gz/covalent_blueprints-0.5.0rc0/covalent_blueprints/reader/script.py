# Copyright 2024 Agnostiq Inc.
"""Logical representation of a Covalent script/module."""

import importlib
import os
import sys
import warnings
from contextlib import redirect_stdout
from enum import Enum
from functools import partial
from pathlib import Path
from types import ModuleType
from typing import Callable, Dict, List, Set, Tuple

import covalent_cloud as cc
from covalent._workflow.electron import Electron
from covalent._workflow.lattice import Lattice
from covalent_cloud.dispatch_management.interface_functions import dispatch
from covalent_cloud.function_serve.deployment import deploy
from covalent_cloud.function_serve.service_class import FunctionService
from covalent_cloud.shared.classes.exceptions import CovalentSDKError
from covalent_cloud.shared.classes.helpers import check_env_is_ready
from covalent_cloud.shared.schemas.volume import Volume
from pkg_resources import Requirement
from pydantic.dataclasses import dataclass

from covalent_blueprints import __file__ as blueprints_file
from covalent_blueprints.logger import bp_log
from covalent_blueprints.reader.capture import (
    CapturedCloudExecutorArguments,
    CapturedCreateEnvArguments,
    CapturedDeployArguments,
    CapturedDispatchArguments,
    CapturedLatticeDeclaration,
    CapturedVolumeArguments,
    capture_cloud_calls,
)
from covalent_blueprints.reader.utilities import custom_build_graph

_BUILDING_BLOCK_TYPES = {Electron, Lattice, FunctionService}
_BLUEPRINTS_PKG = "covalent-blueprints"
try:
    _MIN_VERSION = (Path(blueprints_file).parent.parent / "VERSION").read_text().strip()
except FileNotFoundError:
    _MIN_VERSION = ""

_BLUEPRINTS_PKG_LATEST = (
    f"{_BLUEPRINTS_PKG}>={_MIN_VERSION}" if _MIN_VERSION else _BLUEPRINTS_PKG
)


class ScriptType(Enum):
    """Enumerates the type of Covalent scripts in terms of the main
    function call."""

    DISPATCH = "dispatch"
    DEPLOY = "deploy"


class BlueprintValidationError(Exception):
    """Base class for all blueprint exceptions."""


@dataclass(config={"arbitrary_types_allowed": True})
class CovalentScript:
    """Represents a Covalent workflow or service scripts (.py
    file)"""

    electrons: Dict[str, Callable]
    services: Dict[str, FunctionService]
    lattices: List[CapturedLatticeDeclaration]
    sublattices: Set[str]
    executors: List[CapturedCloudExecutorArguments]
    dispatches: List[CapturedDispatchArguments]
    dispatch_inputs: List[Tuple]
    deploys: List[CapturedDeployArguments]
    deploy_inputs: List[Tuple]
    volumes: List[CapturedVolumeArguments]
    environments: List[CapturedCreateEnvArguments]
    source: Path
    module: ModuleType

    def __post_init__(self):
        self._wrapper = None  # Callable - either `cc.dispatch` or `cc.deploy`
        self._script_type = None  # ScriptType - 'dispatch' or 'deploy'
        self._ready_envs = set()  # Set[str] - names of ready environments

        # Validate collection and enforce assumptions.

        if len(self.dispatches) > 1:
            raise BlueprintValidationError(
                "Can't convert covalent script with more than one `cc.dispatch` call."
            )
        if len(self.deploys) > 1:
            raise BlueprintValidationError(
                "Can't convert covalent script with more than one `cc.deploy` call. "
                "Use a lattice to deploy multiple services inside a recipe."
            )
        if len(self.dispatches) == 1 and len(self.deploys) == 1:
            raise BlueprintValidationError(
                "Can't convert covalent script with both `cc.dispatch` and "
                "`cc.deploy` calls. Consider deploying services inside the lattice."
            )
        if len(self.dispatches) == 0 and len(self.deploys) == 0:
            raise BlueprintValidationError(
                "Can't convert covalent script without a `cc.dispatch` "
                "nor `cc.deploy` call."
            )

        # Check that all envs used in the script are declared in the script
        for ex in self.executors:
            if ex.env == "default":
                continue
            if ex.env not in [env.name for env in self.environments]:
                raise BlueprintValidationError(
                    f"Environment '{ex.env}' is not created in the script. "
                )

        # Check that all env creation calls have the latest blueprints package
        for env in self.environments:
            if not any(Requirement(r).name == _BLUEPRINTS_PKG for r in env.pip):
                raise BlueprintValidationError(
                    f"Environment '{env.name}' should have '{_BLUEPRINTS_PKG}' "
                    f"as a pip dependency, e.g. '{_BLUEPRINTS_PKG_LATEST}'."
                )

    @property
    def type(self) -> ScriptType:
        """Whether the script is a dispatch or deploy script."""
        if self._script_type is None:
            if len(self.dispatches) == 1:
                self._script_type = ScriptType.DISPATCH
            elif len(self.deploys) == 1:
                self._script_type = ScriptType.DEPLOY
            else:
                raise self._indeterminate_type_error()

        return self._script_type

    @property
    def wrapper(self) -> Callable:
        """Either `cc.dispatch` or `cc.deploy`, depending on the
        script."""
        if self.type == ScriptType.DISPATCH:
            return partial(dispatch, volume=self.dispatches[0].volume)

        if self.type == ScriptType.DEPLOY:
            return partial(deploy, volume=self.deploys[0].volume)

        raise self._indeterminate_type_error()

    @property
    def core_function_inputs(self) -> Tuple:
        """The inputs to the main lattice or main function
        service."""
        if self.type == ScriptType.DISPATCH:
            return self.dispatch_inputs[0]

        if self.type == ScriptType.DEPLOY:
            return self.deploy_inputs[0]

        raise self._indeterminate_type_error()

    @property
    def volume(self) -> Volume:
        """The volume attached at dispatch or deploy."""
        if self.type == ScriptType.DISPATCH:
            return self.dispatches[0].volume

        if self.type == ScriptType.DEPLOY:
            return self.deploys[0].volume

        raise self._indeterminate_type_error()

    def get_core_function(self) -> Callable:
        """Either the main lattice or the main function service,
        including post-build updates."""

        bp_log.debug(
            "Getting core function for script '%s' ('%s')",
            self.source.name,
            self.type.value,
        )

        if self.type == ScriptType.DISPATCH:
            lattice_func = self.dispatches[0].lattice_func
            lattice_func_name = lattice_func.__name__
            return self._get_captured_lattice(lattice_func_name).lattice_obj

        if self.type == ScriptType.DEPLOY:
            function_service = self.deploys[0].function_service
            return self.services[function_service.func_name]

        raise self._indeterminate_type_error()

    def get_cloud_executable(self, *args, **kwargs) -> Callable:
        """Either `cc.dispatch(core_lattice)` or
        `cc.deploy(core_service)`"""
        func = self.get_core_function()

        if self.type == ScriptType.DISPATCH:
            # The top level lattice is built locally during dispatch.
            # The following makes sure overloaded resources are applied.
            bp_log.debug(
                "Running custom_build_graph locally on lattice '%s'", func.__name__
            )
            custom_build_graph(func, self.electrons, *args, **kwargs)  # type: ignore

        return self.wrapper(func)

    def create_envs(self, wait: bool = True) -> None:
        """Create the environments used in the script."""
        with open(os.devnull, "w") as devnull:
            with redirect_stdout(devnull):

                for env in self.environments:
                    if self._env_is_ready(env.name, wait=False):
                        continue

                    # Async env creation.
                    kwargs = env.__dict__.copy()
                    kwargs["wait"] = False  # ensure non-blocking
                    cc.create_env(**kwargs)
        if wait:
            # Wait for environments to be ready.
            for env in self.environments:
                ready = self._env_is_ready(env.name, wait=True)
                if not ready:
                    warnings.warn(
                        f"Failed to create environment '{env.name}'.",
                    )

    def delete_envs(self) -> None:
        """Delete ready environments."""
        for env_name in self._ready_envs:
            cc.delete_env(env_name)

    def _env_is_ready(self, env_name: str, wait: bool) -> bool:
        """Check if an environment is ready."""
        if env_name in self._ready_envs:
            return True
        try:
            ready, _ = check_env_is_ready(env_name, wait=wait)
            if ready:
                self._ready_envs.add(env_name)
            return ready
        except CovalentSDKError:
            return False

    def _get_captured_lattice(self, lattice_name: str) -> CapturedLatticeDeclaration:
        """Get the captured lattice object by name."""
        try:
            return next(
                cl
                for cl in self.lattices
                if cl._func.__name__ == lattice_name  # pylint: disable=protected-access
            )
        except StopIteration as e:
            raise ValueError(
                f"No captured declaration for lattice '{lattice_name}'"
            ) from e

    def _indeterminate_type_error(self) -> RuntimeError:
        return RuntimeError("Can't determine whether to dispatch or deploy script.")

    @staticmethod
    def _read(module) -> Tuple[dict, dict]:
        """Extract any electrons or services from the module.

        Must call inside `capture_cloud_calls` context to avoid
        initializing real cloud resources.
        """

        electrons = {}
        services = {}

        # Collect covalent objects.
        for obj_name, obj in module.__dict__.items():

            # Check each object.
            if not callable(obj):
                continue
            if (type_ := _get_callable_type(obj)) not in _BUILDING_BLOCK_TYPES:
                continue

            # Sort each object.
            if type_ is Electron:
                electrons[obj_name] = obj

            elif type_ is FunctionService:
                services[obj_name] = obj

        return electrons, services

    @staticmethod
    def patched_import_module(module_path: Path) -> Tuple[ModuleType, dict]:
        """Import module with cloud calls disabled and Covalent
        object captured."""
        sys_path = sys.path.copy()
        sys.path.append(str(module_path.parent))

        module_name = module_path.with_suffix("").name
        with capture_cloud_calls() as script_data:
            if module_name not in sys.modules:
                module = importlib.import_module(module_name)
            else:
                module = importlib.reload(sys.modules[module_name])

        sys.path = sys_path

        return module, script_data

    @classmethod
    def from_module(cls, module_path: Path) -> "CovalentScript":
        """Convert a module (covalent script) into a `CovalentScript`
        object."""

        module, script_data = cls.patched_import_module(module_path)
        electrons, services = CovalentScript._read(module)

        return cls(
            electrons=electrons,
            services=services,
            source=module_path.absolute(),
            module=module,
            **script_data,
        )


def _get_callable_type(func):
    return Electron if hasattr(func, "electron_object") else type(func)
