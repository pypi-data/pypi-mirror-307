# Copyright 2024 Agnostiq Inc.
"""Templates for Covalent scripts that deploy a single service."""

from typing import Type

from covalent_cloud.cloud_executor.cloud_executor import CloudExecutor

from covalent_blueprints.blueprints.blueprints import CovalentBlueprint
from covalent_blueprints.blueprints.executor_map import ExecutorMap
from covalent_blueprints.reader.script import CovalentScript

# pylint: disable=unnecessary-dunder-call


class SingleServiceExecutorMap(ExecutorMap):
    """Thin wrapper mostly for convenient auto-completions."""

    def __init__(self, script: CovalentScript):
        super().__init__(script)
        self._executor_key = ""

    @property
    def service_executor(self) -> CloudExecutor:
        """Executor for the single service deployment."""
        if not self._executor_key:
            raise ValueError("Please set the executor map's executor key.")
        return self.__getitem__(self._executor_key)

    @service_executor.setter
    def service_executor(self, executor: CloudExecutor) -> None:
        if not self._executor_key:
            raise ValueError("Please set the executor map's executor key.")
        self.__setitem__(self._executor_key, executor)

    def set_executor_key(self, executor_key: str) -> None:
        """Set the executor key for the single service deployment."""
        self._executor_key = executor_key


class SingleServiceBlueprint(CovalentBlueprint):
    """A runnable blueprint that represents a a single service
    deployment."""

    executor_map_type: Type = SingleServiceExecutorMap

    @property
    def executors(self) -> SingleServiceExecutorMap:
        return self._executors
