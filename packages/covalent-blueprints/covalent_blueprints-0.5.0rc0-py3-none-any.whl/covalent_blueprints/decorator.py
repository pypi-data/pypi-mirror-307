# Copyright 2024 Agnostiq Inc.
"""Blueprint decorator."""

from functools import wraps

from covalent_blueprints.blueprints.utilities import (
    get_input_docs,
    get_kwargs,
    get_usage_example,
)


def blueprint(title: str = ""):
    """Decorator for Covalent Blueprint initializer functions. This decorator
    auto-sets the title and other metadata for the blueprint.

    Args:
        title: Optional title for the Blueprint. Defaults to the initializer
            function's name.
    """

    def blueprint_decorator(initializer_func):

        @wraps(initializer_func)
        def wrapper(*args, **kwargs):

            # Initialize the blueprint
            blueprint_instance = initializer_func(*args, **kwargs)
            # Set metadata
            blueprint_instance.title = title or initializer_func.__name__
            blueprint_instance.example = get_usage_example(initializer_func)
            blueprint_instance.inputs.docs = get_input_docs(initializer_func)
            blueprint_instance.inputs.kwargs = get_kwargs(initializer_func)

            return blueprint_instance

        return wrapper

    return blueprint_decorator
