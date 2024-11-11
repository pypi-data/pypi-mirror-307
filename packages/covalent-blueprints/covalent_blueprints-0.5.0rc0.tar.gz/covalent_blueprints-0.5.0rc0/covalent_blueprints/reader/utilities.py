# Copyright 2024 Agnostiq Inc.
"""Utilities for processing Covalent scripts."""

from typing import Callable, Dict

import covalent as ct
from covalent._workflow.lattice import Lattice

from covalent_blueprints.logger import bp_log


def custom_build_graph(
    lattice_obj: Lattice, electrons: Dict[str, Callable], *args, **kwargs
) -> None:
    """Override the usual `build_graph` method of a lattice to update
    metadata.

    Args:
        lattice_: The lattice object to update.
    """
    # pylint: disable=protected-access
    bp_log.debug(
        "Running native build_graph on lattice\n\n%s",
        lattice_obj.workflow_function_string,
    )

    # Need task_packing "context" like in `cc.dispatch`.
    old_task_packing = ct.get_config("sdk.task_packing")
    ct.set_config("sdk.task_packing", "true")

    # Calling via class avoids recursion errors in sublattice case.
    Lattice.build_graph(lattice_obj, *args, **kwargs)

    ct.set_config("sdk.task_packing", old_task_packing)

    # Map of electron names to updated metadata.
    electron_metadata_dict = {
        name: electron.electron_object.metadata.copy()  # type: ignore
        for name, electron in electrons.items()
    }

    # Map of task group IDs to updated metadata.
    new_executor_data_by_group = {}

    # Identify electron task groups and prepare metadata for them.
    for node_id in lattice_obj.transport_graph._graph.nodes:
        node_dict = lattice_obj.transport_graph._graph.nodes[node_id]
        name = node_dict["name"]

        if new_metadata := electron_metadata_dict.get(name):

            # Prepare metadata for the electron's task group.
            task_group_id = node_dict["task_group_id"]
            new_executor_data_by_group[task_group_id] = new_metadata["executor_data"]

            # Shorten loop to avoid redundant iterations.
            del electron_metadata_dict[name]

        # Exit once all electrons have been processed.
        if not electron_metadata_dict:
            break

    bp_log.debug(
        "Updating executor data for task groups: %s",
        tuple(new_executor_data_by_group.keys()),
    )

    # Loop again to set metadata for task groups.
    for node_id in lattice_obj.transport_graph._graph.nodes:
        node_dict = lattice_obj.transport_graph._graph.nodes[node_id]
        task_group_id = node_dict["task_group_id"]

        if task_group_id in new_executor_data_by_group:

            # Set the electron's executor for tasks in its task group.
            executor_data = new_executor_data_by_group[task_group_id]
            bp_log.debug(
                "Setting executor data for task group %s:\n%s\n\n",
                task_group_id,
                executor_data,
            )
            node_dict["metadata"]["executor_data"] = executor_data

    bp_log.debug(
        "Nullifying build_graph on lattice %s ('%s) after custom_build_graph",
        lattice_obj,
        lattice_obj.__name__,
    )
    setattr(lattice_obj, "build_graph", lambda *_, **__: None)
