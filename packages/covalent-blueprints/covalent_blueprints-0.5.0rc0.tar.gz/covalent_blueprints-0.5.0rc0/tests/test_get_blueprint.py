# Copyright 2024 Agnostiq Inc.
""""Tests for the often-used `get_blueprint` function."""
from pathlib import Path

import pytest

from covalent_blueprints import get_blueprint
from covalent_blueprints.blueprints.blueprints import CovalentBlueprint
from covalent_blueprints.blueprints.templates import (
    ServiceWorkflowBlueprint,
    SingleServiceBlueprint,
)

CWD = Path(__file__).parent


@pytest.mark.parametrize(
    "module_path,_cls",
    [
        (CWD / "samples/_scripts/_deploy_chatbot.py", SingleServiceBlueprint),
    ],
)
def test_get_from_source_script(module_path, _cls):
    """Test getting a blueprint from a source .py file."""

    bp = get_blueprint(module_path=module_path, _cls=_cls)
    assert isinstance(bp, _cls)


@pytest.mark.parametrize(
    "module_path,_cls",
    [
        (CWD / "samples/_notebooks/_basic_notebook.ipynb", CovalentBlueprint),
        (
            CWD / "samples/_notebooks/_image_generator_service.ipynb",
            ServiceWorkflowBlueprint,
        ),
    ],
)
def test_get_from_source_notebook(module_path, _cls):
    """Test getting a blueprint from a source .ipynb file."""

    bp = get_blueprint(module_path=module_path, _cls=_cls)
    assert isinstance(bp, _cls)
