# Copyright 2024 Agnostiq Inc.
"""Module for capturing essential elements from Covalent scripts."""

import contextlib
from datetime import timedelta
from pprint import pformat
from typing import Any, Callable, Dict, List, Optional, Union
from unittest.mock import MagicMock, patch

import covalent_cloud as cc
from covalent._workflow.lattice import Lattice
from covalent_cloud.function_serve.service_class import FunctionService
from covalent_cloud.shared.classes.settings import Settings, settings
from covalent_cloud.shared.schemas.volume import Volume
from pydantic.dataclasses import Field, dataclass

from covalent_blueprints.logger import bp_log

CreateEnvCondaArgs = Optional[Union[str, List[str], Dict[str, List[str]]]]


@dataclass
class CapturedCreateEnvArguments:
    """Arguments captured from `cc.create_env()` calls."""

    name: str
    pip: Optional[Union[str, List[str]]] = Field(default_factory=list)
    conda: CreateEnvCondaArgs = Field(default_factory=list)
    settings: Optional[Settings] = Field(default_factory=lambda: settings)
    wait: Optional[bool] = False
    timeout: Optional[int] = 1800
    base_image: Optional[str] = None
    nvidia: bool = False


@dataclass
class CapturedVolumeArguments:
    """Arguments captured from `cc.volume()` calls."""

    name: str
    vtype: Optional[str] = "OBJECT_STORAGE"
    settings: Optional[Settings] = Field(default_factory=lambda: settings)


@dataclass(config={"arbitrary_types_allowed": True})
class CapturedLatticeDeclaration:
    """Arguments captures from `ct.lattice()` calls."""

    lattice_obj: Lattice
    _func: Callable
    backend: Optional[str] = None
    executor: Optional[Any] = None
    workflow_executor: Optional[Any] = None
    deps_bash: Optional[Any] = None
    deps_pip: Optional[Any] = None
    call_before: Optional[Any] = None
    call_after: Optional[Any] = None
    triggers: Optional[Any] = None

    def get_kwargs(self) -> dict:
        """Return kwargs for lattice decorator."""
        d = self.__dict__.copy()
        d.pop("lattice_obj")
        return d


@dataclass(config={"arbitrary_types_allowed": True})
class CapturedDispatchArguments:
    """Arguments captured from `cc.dispatch()` calls."""

    lattice_func: Callable
    settings: Settings = Field(default_factory=lambda: settings)
    volume: Union[Volume, None] = None


@dataclass(config={"arbitrary_types_allowed": True})
class CapturedDeployArguments:
    """Arguments captured from `cc.deploy()` calls."""

    function_service: FunctionService
    volume: Optional[Volume] = None


@dataclass
class CapturedCloudExecutorArguments:
    """Arguments captured from `cc.CloudExecutor()`
    instantiations."""

    num_cpus: int = 1
    memory: Union[int, str] = 1024
    num_gpus: int = 0
    gpu_type: Union[str, cc.cloud_executor.GPU_TYPE] = ""
    env: str = "default"
    time_limit: Union[int, timedelta, str] = 60 * 30
    volume_id: Optional[int] = None
    settings: Dict = Field(default_factory=settings.model_dump)
    validate_environment: bool = True


@contextlib.contextmanager
def capture_cloud_calls():
    """Context designed to capture Covalent function calls and
    objects instantiations, when a script is imported inside it."""

    # pylint: disable=import-outside-toplevel

    # Aliases for real Covalent functions to avoid patches.
    from covalent._workflow.electron import electron as ct_electron
    from covalent._workflow.lattice import Lattice as ct_Lattice
    from covalent._workflow.lattice import lattice as ct_lattice
    from covalent_cloud.cloud_executor.cloud_executor import (
        CloudExecutor as cc_CloudExecutor,
    )
    from covalent_cloud.volume.volume import volume as cc_volume

    class _Result:
        """Mock result object to patch typical manipulations."""

        # pylint: disable=missing-function-docstring
        @property
        def result(self):
            return self

        @property
        def value(self):
            return None

        def load(self):
            return self

    class _Deployment:
        """Mock deployment object to patch typical manipulations."""

        # pylint: disable=too-few-public-methods

        def __getattribute__(self, name: str) -> None:
            return None

    script_data = {
        "environments": [],
        "volumes": [],
        "lattices": [],
        "sublattices": set(),
        "dispatches": [],
        "deploys": [],
        "dispatch_inputs": [],
        "deploy_inputs": [],
        "executors": [],
    }

    def _capture_create_env(*args, **kwargs):
        captured_env = CapturedCreateEnvArguments(*args, **kwargs)
        bp_log.debug("Captured environment:\n%s", pformat(captured_env.__dict__))
        script_data["environments"].append(captured_env)

    def _capture_volume(*args, **kwargs):
        captured_volume = CapturedVolumeArguments(*args, **kwargs)
        bp_log.debug("Captured volume:\n%s", pformat(captured_volume.__dict__))
        script_data["volumes"].append(captured_volume)
        # Actually create the volume here.
        return cc_volume(*args, **kwargs)

    def _capture_electron_declaration(_func=None, **kwargs):

        def _capture_electron_wrapper(_func=None):
            bp_log.debug("Captured electron wrapper processing: %s", _func)
            if isinstance(_func, ct_Lattice) or (
                hasattr(_func, __name__)
                and _func.__name__ == "_capture_lattice_wrapper"
            ):
                script_data["sublattices"].add(_func.__name__)
                bp_log.debug("Registered sublattice: %s", _func.__name__)

            return ct_electron(_func, **kwargs)

        if _func is None:
            return _capture_electron_wrapper
        return _capture_electron_wrapper(_func)

    def _capture_lattice_declaration(_func=None, **kwargs):

        def _capture_lattice_wrapper(_func=None):
            bp_log.debug("Captured lattice wrapper processing: %s", _func)

            lattice_obj = ct_lattice(_func, **kwargs)
            captured_lattice = CapturedLatticeDeclaration(lattice_obj, _func, **kwargs)
            script_data["lattices"].append(captured_lattice)

            return lattice_obj

        if _func is None:
            return _capture_lattice_wrapper
        return _capture_lattice_wrapper(_func)

    def _capture_dispatch(*args, **kwargs):
        captured_dispatch = CapturedDispatchArguments(*args, **kwargs)
        bp_log.debug("Captured dispatch:\n%s", pformat(captured_dispatch.__dict__))
        script_data["dispatches"].append(captured_dispatch)
        return lambda *a, **k: script_data["dispatch_inputs"].append((a, k))

    def _capture_deploy_inputs(*a, **k):
        bp_log.debug("Captured deploy inputs: %s", (a, k))
        script_data["deploy_inputs"].append((a, k))
        return _Deployment()

    def _capture_deploy(*args, **kwargs):
        captured_deploy_args = CapturedDeployArguments(*args, **kwargs)
        bp_log.debug(
            "Captured deploy call:\n%s", pformat(captured_deploy_args.__dict__)
        )
        script_data["deploys"].append(captured_deploy_args)
        return _capture_deploy_inputs

    def _capture_cloud_executor(*args, **kwargs):
        captured_executor = CapturedCloudExecutorArguments(*args, **kwargs)
        bp_log.debug(
            "Captured cloud executor:\n%s", pformat(captured_executor.__dict__)
        )
        script_data["executors"].append(captured_executor)
        kwargs["validate_environment"] = False
        return cc_CloudExecutor(*args, **kwargs)

    def _error_on_os_dispatch(*_, **__):
        raise ValueError(
            "Detected use of `ct.dispatch`. Please replace with `cc.dispatch`"
        )

    with patch("covalent_cloud.create_env", _capture_create_env), patch(
        "covalent_cloud.volume", _capture_volume
    ), patch("covalent.electron", _capture_electron_declaration), patch(
        "covalent.lattice", _capture_lattice_declaration
    ), patch(
        "covalent_cloud.dispatch", _capture_dispatch
    ), patch(
        "covalent_cloud.deploy", _capture_deploy
    ), patch(
        "covalent_cloud.CloudExecutor", _capture_cloud_executor
    ), patch(
        "covalent_cloud.get_deployment", lambda *_, **__: _Deployment()
    ), patch(
        "covalent_cloud.get_result", lambda *_, **__: _Result()
    ), patch(
        "covalent_cloud.save_api_key", lambda *_, **__: None
    ), patch(
        "builtins.print", MagicMock()
    ), patch(
        "covalent.dispatch", _error_on_os_dispatch
    ):
        yield script_data
