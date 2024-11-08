# Copyright 2024 Agnostiq Inc.
"""Templates for Covalent scripts that run a workflow that executes a
single electron and deploys a single service."""

from typing import Type

from covalent_cloud.cloud_executor.cloud_executor import CloudExecutor

from covalent_blueprints.blueprints.blueprints import CovalentBlueprint
from covalent_blueprints.blueprints.executor_map import ExecutorMap
from covalent_blueprints.reader.script import CovalentScript

# pylint: disable=unnecessary-dunder-call


class ServiceWorkflowExecutorMap(ExecutorMap):
    """Thin wrapper mostly for convenient auto-completions."""

    def __init__(self, script: CovalentScript):
        super().__init__(script)
        self._electron_key = ""
        self._service_key = ""

    @property
    def task_executor(self) -> CloudExecutor:
        """Executor for the electron deployment."""
        if not self._electron_key:
            raise ValueError("Please set the executor map's electron key.")
        return self.__getitem__(self._electron_key)

    @task_executor.setter
    def task_executor(self, executor: CloudExecutor) -> None:
        if not self._electron_key:
            raise ValueError("Please set the executor map's electron key.")
        self.__setitem__(self._electron_key, executor)

    @property
    def service_executor(self) -> CloudExecutor:
        """Executor for the service deployment."""
        if not self._service_key:
            raise ValueError("Please set the executor map's service key.")
        return self.__getitem__(self._service_key)

    @service_executor.setter
    def service_executor(self, executor: CloudExecutor) -> None:
        if not self._service_key:
            raise ValueError("Please set the executor map's service key.")
        self.__setitem__(self._service_key, executor)

    def set_executor_key(self, electron_key: str, service_key: str) -> None:
        """Set the executor keys for the service workflow
        deployment."""
        self._electron_key = electron_key
        self._service_key = service_key


class ServiceWorkflowBlueprint(CovalentBlueprint):
    """A runnable blueprint that represents a workflow that executes
    one electron and deploys one service."""

    executor_map_type: Type = ServiceWorkflowExecutorMap

    @property
    def executors(self) -> ServiceWorkflowExecutorMap:
        return self._executors
