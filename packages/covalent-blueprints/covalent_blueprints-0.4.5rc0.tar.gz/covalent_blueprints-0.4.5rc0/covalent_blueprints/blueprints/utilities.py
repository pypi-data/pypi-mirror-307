# Copyright 2024 Agnostiq Inc.
"""High-level utilities for the Covalent blueprints."""
import inspect
import json
import pydoc
import re
import shutil
import subprocess
import tempfile
import textwrap
import warnings
from pathlib import Path
from subprocess import CalledProcessError
from typing import Any, Callable, Dict, Optional, Type, Union

from covalent_blueprints.blueprints.blueprints import CovalentBlueprint
from covalent_blueprints.logger import bp_log
from covalent_blueprints.reader.script import CovalentScript

BLUEPRINTS_CACHE_DIR = Path.home() / ".cache/covalent/blueprints"
REGISTRY_FILE = BLUEPRINTS_CACHE_DIR / "install_dirs.json"

# Parent path for these is the `covalent_blueprints` package.
FIND_SCRIPTS_PATTERN = r"**/_src/_*.py"
FIND_NOTEBOOKS_PATTERN = r"**/_src/_*.ipynb"

if not REGISTRY_FILE.exists():
    REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(REGISTRY_FILE, "w", encoding="utf-8") as registry_file:
        # Create an empty registry file.
        json.dump({}, registry_file)


def get_blueprint(
    module_path: Union[Path, str],
    skip_shell_commands: bool = True,
    check_installed: bool = True,
    _cls: Type[CovalentBlueprint] = CovalentBlueprint,
) -> Any:
    """Load the Python module at the given path and return a
    CovalentBlueprint object.

    Args:
        module_path: Path to the Python module or Jupyter notebook.
        skip_shell_commands: Skip shell commands inside Jupyter notebooks.
            Defaults to True.
        check_installed: Find installed blueprint if module path does not exist.
            Defaults to True.

    Raises:
        FileNotFoundError: If the module path does not exist nor is an installed
            blueprint.
        ValueError: If the module path extension is neither '.py' nor '.ipynb'.

    Returns:
        A blueprint object.
    """

    if not issubclass(_cls, CovalentBlueprint):
        raise TypeError(
            f"Expected a subclass of CovalentBlueprint, got {_cls.__name__}"
        )

    bp_log.debug(
        "Getting blueprints from module path: %s (type: %s)", module_path, _cls.__name__
    )

    module_path = Path(module_path)

    if not module_path.is_file():
        if not check_installed:
            raise FileNotFoundError(f"File not found: {module_path}")

        # Try to find an installed blueprint.
        if installed_blueprint := find_blueprint(str(module_path), _cls):
            return installed_blueprint
        raise ValueError(_format_installed_not_found_error(module_path))

    # File exists. It must be a Python script or Jupyter notebook.
    if module_path.suffix not in {".py", ".ipynb"}:
        raise ValueError("Only Python scripts or Jupyter notebooks are supported")

    # Handle Jupyter notebooks.
    if module_path.suffix == ".ipynb":
        module_path = _py_file_from_notebook(module_path, skip_shell_commands)

    return _load_blueprint_from_module(module_path, _cls)


def find_blueprint(
    name: str,
    _cls: Type[CovalentBlueprint] = CovalentBlueprint,
) -> Optional[Any]:
    """Load the installed blueprint with the given name and return a
    CovalentBlueprint object.

    Args:
        name: Name of the installed blueprint.

    Returns:
        A blueprint object or None if the blueprint is not found.
    """

    installed_blueprints = _find_installed_blueprints()
    module_path = installed_blueprints.get(name)

    if module_path is None:
        bp_log.debug("Blueprint '%s' not found", name)
        return None

    if module_path.suffix == ".ipynb":
        module_path = _py_file_from_notebook(module_path, skip_shell_commands=True)

    return _load_blueprint_from_module(module_path, _cls)


def _load_blueprint_from_module(
    module_path: Path,
    _cls: Type[CovalentBlueprint] = CovalentBlueprint,
) -> CovalentBlueprint:
    """Helper to load a blueprint from a path to a Python module."""

    script = CovalentScript.from_module(module_path)
    executor_map = _cls.create_executor_map(script)
    blueprint = _cls(module_path.stem, script, executor_map)

    return blueprint


def _py_file_from_notebook(
    notebook_path: Path, skip_shell_commands: bool = True
) -> Path:
    """Helper to convert Jupyter notebook into Python file."""

    try:
        subprocess.run(
            ["which", "jupyter-notebook"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
    except CalledProcessError as e:
        raise RuntimeError(
            "Jupyter-notebook is required to convert notebooks to python scripts. "
            "Please retry after installing it with `pip install jupyterlab`."
        ) from e

    BLUEPRINTS_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    py_file_name = f"{notebook_path.with_suffix('').name}.py"

    with open(notebook_path, "r", encoding="utf-8") as file:
        notebook_dict = json.load(file)

    keep_cells = []
    for cell in notebook_dict["cells"]:
        if not cell["cell_type"] == "code":
            # Skip non-code cells.
            continue

        if (
            (metadata := cell.get("metadata"))
            and "vscode" in metadata
            and metadata["vscode"].get("languageId")
        ):
            # Skip non-python cells.
            continue

        keep_source = []
        for line in cell.get("source", []):
            if skip_shell_commands and line.startswith("!"):
                # Skip shell commands.
                continue

            keep_source.append(line)

        cell["source"] = keep_source
        keep_cells.append(cell)

    notebook_dict["cells"] = keep_cells

    # Write the sanitized notebook to a temp file,
    # then convert temp notebook to script.
    with tempfile.NamedTemporaryFile(mode="w", suffix=".ipynb") as temp_notebook:
        json.dump(notebook_dict, temp_notebook, indent=2)
        temp_notebook.flush()

        # Will save converted script to cache directory.
        py_file_path = BLUEPRINTS_CACHE_DIR / py_file_name

        try:
            # Convert notebook to script.
            cmd = (
                f"jupyter nbconvert --to script {temp_notebook.name} "
                f"--log-level WARN --output {py_file_path.with_suffix('')}"
            )
            subprocess.run(cmd.split(), check=True)
        except CalledProcessError as e:
            raise RuntimeError(
                f"Failed to convert jupyter notebook '{notebook_path!s}' to "
                "python script. "
            ) from e

    return py_file_path


def register_blueprints_dir(
    name: str,
    install_dir: Union[str, Path],
    overwrite: bool = False,
) -> None:
    """Register a directory that contains installed blueprints in
    it's sub- directories. The resolved, absolute path of the
    directory is stored in the registry.

    Registering a directory means adding it to the `instal_dirs.json` file in
    the blueprints cache directory located at
    '$HOME/.cache/covalent/blueprints'.

    Args:
        name: Name of the blueprints collection.
        install_dir: String or path object of the directory containing installed
            blueprints.
        overwrite: Overwrite the existing entry if it exists. Defaults to False.
    """

    if not BLUEPRINTS_CACHE_DIR.is_dir():
        BLUEPRINTS_CACHE_DIR.mkdir(parents=True, exist_ok=True)

    install_dir = Path(install_dir).resolve().absolute()

    # Check if the install directory exists.
    if not install_dir.is_dir():
        raise FileNotFoundError(
            f"Blueprints location '{install_dir}' does not exist or is not a directory"
        )

    # Load the registry.
    with open(REGISTRY_FILE, "r", encoding="utf-8") as file:
        registry_dict = json.load(file)

    # Filter out registered directories that no longer exist.
    keep_keys = []
    for name_, install_dir_ in registry_dict.items():
        if Path(install_dir_).is_dir():
            keep_keys.append(name_)
        else:
            warnings.warn(
                f"Install directory '{install_dir_}' registered under name '{name_}' "
                "no longer exists. Removing from registry."
            )
    registry_dict = {k: v for k, v in registry_dict.items() if k in keep_keys}

    # Check if the name already exists in the registry.
    if not overwrite and name in registry_dict:
        warnings.warn(
            f"Name '{name}' already exists in the registry. "
            "Pass `overwrite=True` to overwrite the existing entry."
        )
        return

    # Check if the install directory already exists in the registry.
    if not overwrite and str(install_dir) in registry_dict.values():
        warnings.warn(
            f"Install directory '{install_dir!s}' already exists in the registry "
            f"under name '{name}'."
        )
        if str(install_dir.absolute()) == registry_dict.get(name):
            # Already registered.
            return

    # Update the registry
    registry_dict[name] = str(install_dir)

    # Update the registry file.
    with open(REGISTRY_FILE, "w", encoding="utf-8") as file:
        json.dump(registry_dict, file, indent=2)


def _find_installed_blueprints() -> Dict[str, Path]:
    """Find all the blueprints in the covalent-blueprints package."""

    # Load the registry.
    with open(REGISTRY_FILE, "r", encoding="utf-8") as file:
        registry_dict = json.load(file)

    # Discover scripts and notebooks
    installed_blueprints = {}
    for name, install_dir in registry_dict.items():
        install_dir = Path(install_dir)
        blueprints_list = []
        blueprints_list.extend(install_dir.glob(FIND_SCRIPTS_PATTERN))
        blueprints_list.extend(install_dir.glob(FIND_NOTEBOOKS_PATTERN))

        bp_log.info("Blueprints found in '%s': %s", name, blueprints_list)
        if not blueprints_list:
            # Skip empty.
            continue

        installed_blueprints[name] = blueprints_list

    discovered_blueprints = {}
    for name, blueprints_list in installed_blueprints.items():
        for blueprint_file in blueprints_list:

            # Remove leading underscore for registered name.
            # Path conversion here is just to remove suffix.
            file_basename = str(Path(blueprint_file.name.lstrip("_")).with_suffix(""))

            file_name = "/".join([name, file_basename])
            discovered_blueprints[file_name] = blueprint_file.absolute()

    return discovered_blueprints


def _format_installed_not_found_error(module_path: Union[str, Path]) -> str:
    """Formats the error message that lists installed blueprints when
    a blueprint is not found."""
    installed_blueprints = _find_installed_blueprints()
    installed_ = []
    for bp_name, path in installed_blueprints.items():
        bp_name = f"'{bp_name}'"
        installed_.append(f"{bp_name}\n    @ {path}\n")

    installed_ = sorted(installed_)
    installed_str = "\n".join(installed_)
    return (
        f"Blueprint '{module_path!s}' not found. Installed blueprints:\n\n"
        f"{installed_str if installed_str.strip() else '[None]'}"
    )


def get_usage_example(func: Callable) -> str:
    """Get the usage example from the docstring of a function with an
    'Example:' section.

    Args:
        func: A function object.

    Returns:
        Usage example substring, or the empty string if no example is
        found.
    """
    doc_heading_pattern = re.compile(r"^(\w+:)($|\n)")
    docstring_lines = pydoc.getdoc(func).splitlines()

    # Find the example section.
    i = 0
    line = ""
    while i < len(docstring_lines):
        line = docstring_lines[i]
        if doc_heading_pattern.match(line) and "Example" in line:
            break
        i += 1

    # If no example section is found, return an empty string.
    if i == len(docstring_lines) - 1:
        return ""

    # Determine the indent level of the example heading;
    # allows example to exist in the middle of docstring.
    heading_indent_level = len(line) - len(line.lstrip())

    # Proceed past the example heading itself.
    i += 1

    # Extract example lines.
    example_lines = []
    for line in docstring_lines[i:]:

        line_indent_level = len(line) - len(line.lstrip())
        if line and line_indent_level <= heading_indent_level:
            # Stop at the next dedent.
            break

        if doc_heading_pattern.match(line):
            # Stop at the next heading.
            break

        example_lines.append(line)

    # Clean up the example string.
    example_string = "\n".join(example_lines)
    example_string = textwrap.dedent(example_string)
    example_string = example_string.strip(" `\n").strip()

    return example_string


def get_kwargs(func: Callable) -> Dict[str, Any]:
    """Get a dictionary of keyword arguments and their default values.

    Args:
        initializer_function: _description_

    Raises:
        ValueError: when the function has arguments with no default value.

    Returns:
        A dictionary of keyword arguments and their default values.
    """
    signature = inspect.signature(func)
    params = signature.parameters
    var_kinds = [inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD]

    keyword_params = {}
    for k, v in params.items():
        if v.default != inspect.Parameter.empty:
            keyword_params[k] = v.default
        elif v.kind not in var_kinds:
            raise ValueError(
                f"Initializer function '{func.__name__}' has "
                f"an argument '{k}' with no default value."
            )

    return keyword_params


def get_input_docs(func: Callable) -> Dict[str, Optional[str]]:
    """Get a dictionary mapping parameter names to their
    documentation.

    Args:
        func: A function object.

    Returns:
        A dictionary mapping parameter names to their documentation.
    """
    signature = inspect.signature(func)
    signature_param_names = set(signature.parameters)
    arg_start_pattern = re.compile(r"^\s*\**(\w+):\s*(.*)")
    docstring = pydoc.getdoc(func)

    if not docstring:
        warnings.warn(f"No docstring found for function '{func.__name__}'")
        return {param: None for param in signature_param_names}

    docstring_lines = textwrap.dedent(docstring).splitlines()
    current_param_name = None
    params_dict = {}

    for line in docstring_lines:
        stripped_line = line.strip()

        if not stripped_line:
            current_param_name = None

        elif match_ := arg_start_pattern.match(line):
            # Starting to parse new parameter documentation.
            param_name = match_.group(1)

            if param_name not in signature_param_names:
                # Misidentified as parameter or extra parameter in docstring.
                continue

            param_kind = signature.parameters[param_name].kind
            if param_kind == inspect.Parameter.VAR_POSITIONAL:
                param_name = "*" + param_name
            elif param_kind == inspect.Parameter.VAR_KEYWORD:
                param_name = "**" + param_name

            # Record first line in doc for parameter.
            params_dict[param_name] = [match_.group(2)]
            current_param_name = param_name

        elif current_param_name:
            params_dict[current_param_name].append(stripped_line)

    # Check for any missing parameters in the docstring
    missing_params = signature_param_names - params_dict.keys()
    for missing_param in missing_params:
        if signature.parameters[missing_param].kind not in [
            inspect.Parameter.VAR_POSITIONAL,
            inspect.Parameter.VAR_KEYWORD,
        ]:
            warnings.warn(
                f"Parameter '{missing_param}' in function signature of "
                f"'{func.__name__}' is not documented."
            )

    return {k: " ".join(lines) for k, lines in params_dict.items()}


def pick_largest_fs(*dirs) -> Path:
    """Returns the path residing in the largest filesystem.

    If multiple paths are equally large, the first one is returned.
    """
    largest_free_space = -1
    largest_dir = None

    for dir_ in dirs:
        dir_path = Path(dir_).expanduser().absolute()
        try:
            free_space = shutil.disk_usage(dir_path).free
            if free_space > largest_free_space:
                largest_free_space = free_space
                largest_dir = dir_path
        except (FileNotFoundError, PermissionError):
            continue

    if largest_dir is None:
        raise FileNotFoundError(f"No valid directory among {dirs}")

    return largest_dir
