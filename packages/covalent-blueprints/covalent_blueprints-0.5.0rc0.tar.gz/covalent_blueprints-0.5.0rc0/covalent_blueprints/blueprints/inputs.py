# Copyright 2024 Agnostiq Inc.
"""Arguments for Covalent blueprints."""
from pprint import pformat
from typing import Dict, Optional

from covalent_blueprints.reader.script import CovalentScript


class BlueprintInputs:
    """Provides arguments interface for Covalent blueprints."""

    def __init__(self, script: CovalentScript):
        self._docs: Dict[str, Optional[str]] = {}

        # Arguments for the wrapped lattice or service
        self._core_args, self._core_kwargs = script.core_function_inputs

        if not self._core_args == ():
            raise ValueError(
                "Please avoid positional arguments in the core function "
                "(lattice or service) wrapped by the blueprint."
            )

        # Keyword arguments for the blueprint initializer.
        # These are set by the @blueprint decorator.
        self._kwargs: dict = {}

    @property
    def core_kwargs(self):
        return self._core_kwargs

    @core_kwargs.setter
    def core_kwargs(self, value: dict):
        if isinstance(value, dict):
            self._core_kwargs = value
        else:
            raise ValueError("core_kwargs must be a dict")

    @property
    def kwargs(self) -> dict:
        """Default keyword arguments for the blueprint's core
        function."""
        return self._kwargs

    @kwargs.setter
    def kwargs(self, value: dict) -> None:
        if isinstance(value, dict):
            self._kwargs = value
        else:
            raise ValueError("kwargs must be a dict")

    @property
    def docs(self) -> Dict[str, Optional[str]]:
        """Documentation for the arguments."""
        return self._docs.copy()

    @docs.setter
    def docs(self, value: dict) -> None:
        self._docs = value

    def to_dict(self):
        """Return the arguments as a dictionary."""
        return {"kwargs": self.kwargs.copy(), "docs": self.docs.copy()}

    def override_core_defaults(self, kwargs) -> dict:
        """Override the default arguments with the provided
        kwargs."""
        new_kwargs = self._core_kwargs.copy()
        new_kwargs.update(**kwargs)

        return new_kwargs

    def __getitem__(self, key):
        if key == "args":
            return self._core_args
        if key == "kwargs":
            return self.kwargs
        raise KeyError(f"Invalid key '{key}'")

    def __repr__(self):
        return f"BlueprintInputs({self.kwargs})"

    def __str__(self):
        return pformat(self.to_dict())
