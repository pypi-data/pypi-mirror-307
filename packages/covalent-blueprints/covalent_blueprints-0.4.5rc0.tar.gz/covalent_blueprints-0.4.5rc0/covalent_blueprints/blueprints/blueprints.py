# Copyright 2024 Agnostiq Inc.
"""Implementation of the main blueprint object."""

import os
from functools import partial
from typing import Any, Dict, Generic, List, Tuple, Type, TypeVar, Union

import cloudpickle
from covalent._results_manager.result import Result
from covalent._shared_files.context_managers import active_lattice_manager
from covalent._workflow.electron import Electron, electron
from covalent._workflow.lattice import lattice
from covalent_cloud.dispatch_management.interface_functions import get_result
from covalent_cloud.function_serve.deployment import Deployment, get_deployment
from covalent_cloud.service_account_interface.auth_config_manager import get_api_key
from covalent_cloud.shared.schemas.volume import Volume

from covalent_blueprints.blueprints.executor_map import ExecutorMap
from covalent_blueprints.blueprints.inputs import BlueprintInputs
from covalent_blueprints.blueprints.summary import BlueprintSummary
from covalent_blueprints.logger import bp_log
from covalent_blueprints.reader.script import CovalentScript, ScriptType
from covalent_blueprints.reader.utilities import custom_build_graph

API_KEY_ENV_VAR = "CC_API_KEY"

MISSING_API_KEY_MESSAGE = f"""
Covalent Cloud API key is not set.
Please copy your API key from the Covalent Cloud Dashboard and either run:

    >>> from covalent_blueprints import save_api_key
    >>> save_api_key("<you-api-key>")

or set the environment variable in your shell:

    $ export {API_KEY_ENV_VAR}="<your-api-key>".

Note that the environment variable will override any saved API key.
""".strip()


M = TypeVar("M", bound=ExecutorMap)


class CovalentBlueprint(Generic[M]):
    """A runnable blueprint that represents a Covalent workflow or service."""

    executor_map_type: Type = ExecutorMap

    @classmethod
    def create_executor_map(cls, script: CovalentScript) -> M:
        """Create an executor map for this blueprint."""
        return cls.executor_map_type(script)

    def __init__(self, name: str, script: CovalentScript, executor_map: M):
        self._name = name
        self._title = ""
        self._script = script
        self._inputs = BlueprintInputs(script)
        self._executors = executor_map
        self._ids: List[Tuple[str, str]] = []
        self._example = ""
        self._description = ""

        bp_log.info(
            "Initialized blueprint '%s' with script source %s", self.name, script.source
        )

    @property
    def name(self) -> str:
        """Name of the original Covalent script."""
        return self._name.lstrip("_")

    @property
    def title(self) -> str:
        """Displayed title of the blueprint."""
        return self._title or self.name

    @title.setter
    def title(self, title: str) -> None:
        self._title = title

    @property
    def executors(self) -> M:
        """A map from electron/service names to corresponding executors."""
        return self._executors

    @property
    def environments(self) -> List[Dict[str, Any]]:
        """A map from environment names to corresponding environment
        strings."""
        return [
            {k: v for k, v in env.__dict__.items() if k != "settings"}
            for env in self._script.environments
        ]

    @property
    def volume(self) -> Union[Volume, None]:
        """Volume object for the blueprint."""
        return self._script.volume

    @property
    def volumes(self) -> List[Dict[str, Any]]:
        """A map from volume names to corresponding volume strings."""
        omit_keys = ["settings", "vtype"]
        return [
            {k: v for k, v in volume.__dict__.items() if k not in omit_keys}
            for volume in self._script.volumes
        ]

    @property
    def inputs(self) -> BlueprintInputs:
        """Inputs to the blueprint."""
        return self._inputs

    @property
    def ids(self) -> List[Tuple[str, str]]:
        """Dispatch and/or function IDs of workflow results and/or
        deployments."""
        return self._ids.copy()

    @property
    def example(self) -> str:
        """Example usage of the blueprint."""
        return self._example

    @example.setter
    def example(self, example: str) -> None:
        self._example = example

    @property
    def description(self) -> str:
        """Description of the blueprint."""
        return self._description or self._script.module.__doc__ or ""

    @description.setter
    def description(self, description: str) -> None:
        if self._description:
            raise ValueError(
                f"Blueprint '{self.name}' already has a description. "
                "Consider editing the module docstring of the source script."
            )
        self._description = description

    def set_default_inputs(self, **kwargs) -> None:
        """Call this method with any kwargs to set the default inputs for the
        blueprint."""
        if len(kwargs) != 0:
            self.inputs.core_kwargs = kwargs

    def _check_api_key(self) -> None:
        api_key = os.getenv("CC_API_KEY") or get_api_key()
        if not api_key:
            raise ValueError(MISSING_API_KEY_MESSAGE)
        bp_log.info("Found API key: %s", api_key[:4] + "*" * len(api_key[4:]))

    def _rebuild(self) -> None:
        """Rebuild blueprint components by modifying tasks and services in
        place."""

        bp_log.info("Registering pickle by value for module: %s", self._script.source)
        cloudpickle.register_pickle_by_value(self._script.module)

        executors_dict = self._executors.map

        # Electrons
        for electron_name, electron_ in self._script.electrons.items():
            # Create replacement electron.
            new_executor = executors_dict[electron_name]
            new_electron = electron(electron_, executor=new_executor)

            # Update object data; used to update the transport graph at runtime.
            electron_.electron_object = new_electron.electron_object  # type: ignore

        # Services
        for service_name, service_ in self._script.services.items():
            service_.executor = executors_dict[service_name]

        # Lattices
        for captured_lattice_ in self._script.lattices:

            # Replace with new lattice object.
            new_lattice = lattice(**captured_lattice_.get_kwargs())

            if captured_lattice_.lattice_obj.__name__ not in self._script.sublattices:
                bp_log.debug(
                    "Replacing lattice '%s' ('%s') with new lattice",
                    captured_lattice_.lattice_obj,
                    captured_lattice_.lattice_obj.__name__,
                )
                captured_lattice_.lattice_obj = new_lattice
                bp_log.debug(
                    "New lattice '%s' ('%s')",
                    captured_lattice_.lattice_obj,
                    captured_lattice_.lattice_obj.__name__,
                )
            else:
                bp_log.debug(
                    "Overwriting (instead of replacing) lattice"
                    " '%s' ('%s') - is sublattice",
                    captured_lattice_.lattice_obj,
                    captured_lattice_.lattice_obj.__name__,
                )
                captured_lattice_.lattice_obj.__dict__ = new_lattice.__dict__.copy()

            bp_log.debug(
                "Overriding build_graph on lattice object %s ('%s')",
                captured_lattice_.lattice_obj,
                captured_lattice_.lattice_obj.__name__,
            )
            captured_lattice_.lattice_obj.build_graph = partial(  # type: ignore
                custom_build_graph,
                captured_lattice_.lattice_obj,
                self._script.electrons,
            )

    def build(self) -> None:
        """Prepare the blueprint for execution."""
        bp_log.info("Checking for API key...")
        self._check_api_key()  # API key is required for envs and volumes

        bp_log.info("Creating environments for blueprint '%s'", self.name)
        self._script.create_envs()

        bp_log.info("Building blueprint '%s'", self.name)
        self._rebuild()

    def run(
        self, *args, wait_for_result: bool = True, **kwargs
    ) -> Union[str, Result, Deployment]:
        """Run the underlying workflow dispatch or service deployment in the
        cloud. Positional and keyword arguments override the default inputs set
        in the blueprint.

        Args:
            wait_for_result: Wait for the workflow to complete or the deployment
                to reach an active state. Set to False to run asynchronously.
                Defaults to True.

        Returns:
            If wait_for_result is True, the workflow result or deployment client
            is returned. Otherwise, the workflow dispatch ID or a not-yet-active
            deployment client is returned. Use `cc.get_result` or
            `cc.get_deployment` with `wait=True` to retrieve the final result or
            active deployment.
        """
        if args:
            raise ValueError(self._args_not_allowed_error())

        if active_lattice_manager.get_active_lattice() is not None:
            raise RuntimeError(
                "The .run() method is not allowed inside a Covalent lattice. "
                "Please call the blueprint directly instead."
            )

        self.build()
        kwargs = self.inputs.override_core_defaults(kwargs)

        # Execute
        bp_log.debug("Running blueprint '%s' with\nkwargs: %s", self.name, kwargs)
        cloud_executable = self._script.get_cloud_executable(**kwargs)
        handle = cloud_executable(**kwargs)

        # Record the dispatch or deployment ID
        id_ = handle.function_id if isinstance(handle, Deployment) else handle
        self._ids.append((self._script.type.value, id_))

        bp_log.info("Cloud executing blueprint '%s' (ID: %s)", self.name, id_)

        if not wait_for_result:
            return handle

        if self._script.type == ScriptType.DISPATCH:
            return _get_result_with_retries(handle)

        if self._script.type == ScriptType.DEPLOY:
            return get_deployment(handle, wait=True)

        raise ValueError("Unknown type of cloud executable")

    def __call__(self, *args, **kwargs) -> Electron:
        """Run the blueprint as an electron or sub-lattice.

        This method does not run the blueprint in the cloud, unless it
        is used inside a lattice.
        """
        if args:
            raise ValueError(self._args_not_allowed_error())

        if active_lattice_manager.get_active_lattice() is None:
            raise RuntimeError(
                "Calling a blueprint directly is not allowed outside a "
                "Covalent lattice. Please use the .run() method instead."
            )

        self.build()
        kwargs = self.inputs.override_core_defaults(kwargs)
        core_function = self._script.get_core_function()

        bp_log.debug("Calling blueprint '%s' with kwargs: %s", self.name, kwargs)

        if self._script.type == ScriptType.DISPATCH:
            bp_log.debug(
                "Creating sublattice from core function '%s' for blueprint '%s'",
                core_function,
                self.name,
            )
            return electron(core_function)(**kwargs)

        if self._script.type == ScriptType.DEPLOY:
            return core_function(**kwargs)

        raise ValueError("Unknown type of cloud executable")

    def summary(self, get_source: bool = False) -> Dict[str, Any]:
        """Get a summary of the blueprint.

        Args:
            get_source: Include the content of the source file.
            Defaults to False.

        Returns:
            A dictionary with the blueprint summary.
        """
        summary_ = BlueprintSummary(
            name=self.name,
            title=self.title,
            description=self.description,
            type=self._script.type.value,
            inputs=self.inputs.to_dict(),
            executors={k: v.__dict__ for k, v in self.executors.map.items()},
            environments=self.environments,
            volumes=[volume["name"] for volume in self.volumes],
            example=self.example,
            source_file=str(self._script.source),
        )
        if get_source:
            summary_.get_source()

        return summary_.model_dump()

    def _args_not_allowed_error(self):
        """Formats error message for non-empty positional arguments."""
        kwarg_docs = []
        for k, v in self.inputs.docs.items():
            kwarg_docs.append(f"    {k}: {v}")

        kwargs_msg = "\n".join(kwarg_docs)

        return (
            "Blueprint execution calls must not have positional arguments. "
            "Please use keyword arguments instead."
            "\n\n"
            f"Available keyword arguments:\n\n{kwargs_msg}"
            "\n\n"
            "Positional arguments are only valid during blueprint initialization."
        )


def _get_result_with_retries(
    dispatch_id: str, max_loops: int = 5
) -> Union[Result, None]:
    """Get the result of a workflow dispatch, with retries to avoid recursion
    errors."""
    loops = 0
    while loops < max_loops:
        try:
            res = get_result(dispatch_id, wait=True)
            res.result.load()

            return res.result.value

        except RecursionError:
            pass

        finally:
            loops += 1

    raise TimeoutError(
        f"""Result for dispatch is still not available. To continue waiting, run:

    import covalent_cloud as cc

    res = cc.get_result("{dispatch_id}", wait=True)
    res.result.load()
    result = res.result.value

"""
    )
