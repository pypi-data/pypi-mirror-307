# Copyright 2024 Agnostiq Inc.
""""Tests for blueprint execution settings - inside/outside a lattice."""
import io
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import covalent as ct
import covalent_cloud as cc
import pytest

from covalent_blueprints import get_blueprint
from covalent_blueprints.blueprints.templates import SingleServiceBlueprint

CWD = Path(__file__).parent


class _ForceStop(Exception):
    """Use to prevent actual dispatches in tests."""


def _stop_build(*_, **__):
    raise _ForceStop("This is a test.")


def test_run_inside_lattice_fails():
    """Test that .run() is disallowed inside a lattice."""

    module_path = CWD / "samples/_scripts/_deploy_chatbot.py"
    _cls = SingleServiceBlueprint
    ex = cc.CloudExecutor(validate_environment=False)

    chatbot_bp = get_blueprint(module_path=module_path, _cls=_cls)

    @ct.lattice(executor=ex, workflow_executor=ex)
    def _lattice_1():
        return chatbot_bp.run()  # RuntimeError

    buffer = io.StringIO()

    try:
        with patch.object(chatbot_bp, "build", new=_stop_build):

            with pytest.raises(_ForceStop):
                # Confirm patch, no real dispatch will happen.
                chatbot_bp.build()

            with redirect_stdout(buffer):
                # Outermost patch ensures this will raise _ForceStop
                # if RuntimeError is missed.
                cc.dispatch(_lattice_1)()

    except _ForceStop:
        # Avoid real dispatch if missed RuntimeError.
        pass

    printed_msg = buffer.getvalue()
    expected_msg = "ERROR: The .run() method is not allowed inside a Covalent lattice."

    debug_msg = f"Expected: '{expected_msg}', Got: '{printed_msg}'"
    assert expected_msg in buffer.getvalue(), debug_msg


def test_call_outside_lattice_fails():
    """Test that .__call__() is disallowed outside a lattice."""

    module_path = CWD / "samples/_scripts/_deploy_chatbot.py"
    _cls = SingleServiceBlueprint

    chatbot_bp = get_blueprint(module_path=module_path, _cls=_cls)
    msg = "Calling a blueprint directly is not allowed outside a Covalent lattice."

    try:
        with patch.object(chatbot_bp, "build", new=_stop_build):

            with pytest.raises(_ForceStop):
                # Confirm patch, no real dispatch will happen.
                chatbot_bp.build()

            with pytest.raises(RuntimeError, match=msg):
                # Outermost patch ensures this will raise _ForceStop
                # if RuntimeError is missed.
                chatbot_bp()

    except _ForceStop:
        # Avoid real dispatch if missed RuntimeError.
        pass
