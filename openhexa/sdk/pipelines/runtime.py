"""Utilities used by containerized pipeline runners to import and download pipelines."""

import ast
import base64
import importlib
import io
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from zipfile import ZipFile

import requests

from openhexa.sdk.pipelines.exceptions import InvalidParameterError, PipelineNotFound
from openhexa.sdk.pipelines.parameter import (
    TYPES_BY_PYTHON_TYPE,
    DHIS2Widget,
    IASOWidget,
    Parameter,
    validate_parameters,
)
from openhexa.sdk.utils import Settings

from .pipeline import Pipeline


@dataclass
class Argument:
    """Argument of a decorator."""

    name: str  # Use str instead of string
    types: list[type] = field(default_factory=list)
    default_value: Any = None


def import_pipeline(pipeline_dir_path: str) -> Pipeline:
    """Import pipeline code within provided path using importlib.

    Args:
        pipeline_dir_path: Path to the directory containing the pipeline code

    Returns
    -------
        The imported Pipeline object

    Raises
    ------
        ImportError: If the pipeline module cannot be imported
        ValueError: If no Pipeline object is found in the module
    """
    pipeline_dir = os.path.abspath(pipeline_dir_path)
    sys.path.append(pipeline_dir)
    try:
        pipeline_package = importlib.import_module("pipeline")

        # Find the first Pipeline object in the module
        for _, obj in pipeline_package.__dict__.items():
            if isinstance(obj, Pipeline):
                return obj

        raise ValueError("No Pipeline object found in the imported module")
    except ImportError as e:
        raise ImportError(f"Failed to import pipeline module: {e}")


def download_pipeline(url: str, token: str, run_id: str, target_dir: str) -> None:
    """Download pipeline code and unzip it into the target directory.

    Args:
        url: The base URL for the API
        token: Authentication token
        run_id: ID of the pipeline run
        target_dir: Directory where the pipeline code will be extracted

    Raises
    ------
        requests.RequestException: If the API request fails
        ValueError: If the response data is invalid
    """
    query = """
    query PipelineDownload($id: UUID!) {
      pipelineRun(id: $id) {
        id
        version {
          versionNumber
        }
        code
      }
    }
    """

    try:
        import os

        response = requests.post(
            f"{url}/graphql/",
            headers={"Authorization": f"Bearer {token}"},
            json={"query": query, "variables": {"id": run_id}},
            timeout=30,
            verify=Settings.verify_ssl(),
        )
        response.raise_for_status()

        data = response.json()
        if not data.get("data", {}).get("pipelineRun", {}).get("code"):
            raise ValueError("Invalid response: missing pipeline code")

        zipfile_data = base64.b64decode(data["data"]["pipelineRun"]["code"].encode("ascii"))

        # Use the original directory as a context to return to
        original_dir = os.getcwd()
        try:
            os.chdir(target_dir)
            with ZipFile(io.BytesIO(zipfile_data)) as zf:
                zf.extractall()
        finally:
            os.chdir(original_dir)
    except requests.RequestException as e:
        raise requests.RequestException(f"Failed to download pipeline: {e}")


def _get_decorators_by_name(node: ast.AST, name: str) -> list[ast.Call]:
    """Get all decorators with the specified name from an AST node.

    Args:
        node: The AST node to inspect
        name: The name of the decorator to find

    Returns
    -------
        List of matching decorator Call nodes
    """
    if not hasattr(node, "decorator_list"):
        return []

    return [
        dec
        for dec in node.decorator_list
        if isinstance(dec, ast.Call) and hasattr(dec.func, "id") and dec.func.id == name
    ]


def _get_decorator_arg_value(decorator: ast.Call, arg: Argument, index: int) -> tuple[Any, bool]:
    """Return the value of the argument of the decorator.

    Args:
        decorator: The decorator Call node
        arg: The Argument definition to extract
        index: The position index for positional arguments

    Returns
    -------
        A tuple with the value of the argument and a boolean indicating if
        the argument is a keyword argument.

    Raises
    ------
        ValueError: If the argument type is unsupported
    """
    # First check for keyword arguments
    for keyword in decorator.keywords:
        if keyword.arg == arg.name:
            if type(keyword.value) not in arg.types:
                raise ValueError(
                    f"Unsupported argument type for {arg.name}: {type(keyword.value)}. Expected {arg.types}"
                )
            if isinstance(keyword.value, ast.Constant):
                return (keyword.value.value, True)
            elif isinstance(keyword.value, ast.Name):
                return (keyword.value.id, True)
            elif isinstance(keyword.value, ast.List):
                return ([el.value for el in keyword.value.elts], True)
            elif isinstance(keyword.value, ast.Attribute):
                if keyword.value.attr in DHIS2Widget.__members__:
                    return getattr(DHIS2Widget, keyword.value.attr), True
                elif keyword.value.attr in IASOWidget.__members__:
                    return getattr(IASOWidget, keyword.value.attr), True
                else:
                    raise ValueError(f"Unsupported widget: {keyword.value.attr}")

    # Then check for positional arguments
    try:
        return (decorator.args[index].value, False)
    except IndexError:
        return (arg.default_value, False)


def _get_decorator_spec(decorator: ast.Call, args: tuple[Argument, ...]) -> dict[str, dict[str, Any]]:
    """Build a specification of decorator arguments.

    Args:
        decorator: The decorator Call node
        args: Tuple of Argument definitions to extract

    Returns
    -------
        Dictionary mapping argument names to their values and keyword status
    """
    args_spec = {}
    for i, arg in enumerate(args):
        value, is_keyword = _get_decorator_arg_value(decorator, arg, i)
        args_spec[arg.name] = {"value": value, "is_keyword": is_keyword}
    return args_spec


def get_pipeline(pipeline_path: Path) -> Pipeline:
    """Return the pipeline with metadata and parameters from the pipeline code.

    Args:
        pipeline_path: Path to the pipeline directory

    Raises
    ------
        PipelineNotFound: If no function with openhexa.sdk pipeline decorator is found.
        InvalidParameterError: If the parameter type is invalid/unknown.
        ValueError: If the value of an argument is not a primitive type.

    Returns
    -------
        Pipeline: The pipeline object with parameters and metadata.
    """
    pipeline_file = Path(pipeline_path) / "pipeline.py"

    try:
        with open(pipeline_file) as f:
            tree = ast.parse(f.read())
    except (FileNotFoundError, PermissionError) as e:
        raise PipelineNotFound(f"Could not read pipeline file: {e}")

    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue

        pipeline_decorators = _get_decorators_by_name(node, "pipeline")
        if not pipeline_decorators:
            continue

        pipeline_decorator = pipeline_decorators[0]
        pipeline_args = _get_decorator_spec(
            pipeline_decorator,
            (
                Argument("code", [ast.Constant]),
                Argument("name", [ast.Constant]),
                Argument("timeout", [ast.Constant]),
            ),
        )

        # Extract code and name values for validation
        code_arg = pipeline_args.get("code", {"value": None, "is_keyword": False})
        name_arg = pipeline_args.get("name", {"value": None, "is_keyword": False})

        # Handle deprecated 'code' argument
        if code_arg["value"] is not None:
            if code_arg["is_keyword"]:
                print(
                    "\n\033[93m",
                    f"The 'code' argument is deprecated and should not be used as a keyword. "
                    f"Replace 'code=\"{code_arg['value']}\"' by 'name=\"{code_arg['value']}\"'\033[0m",
                    "\n",
                    flush=True,
                )

            if name_arg["value"] is not None:
                print(
                    "\n\033[93m",
                    f"Providing both 'code' and 'name' is deprecated. "
                    f"Please remove 'code' and only use 'name' when decorating the pipeline: "
                    f'@pipeline(name="{name_arg["value"]}")\033[0m',
                    "\n",
                    flush=True,
                )

        # Determine the pipeline name (prefer 'name', fall back to 'code')
        pipeline_name = name_arg["value"] if name_arg["value"] is not None else code_arg["value"]

        # Extract timeout
        timeout = pipeline_args.get("timeout", {"value": None})["value"]

        # Process parameters
        pipeline_parameters = []
        for parameter_decorator in _get_decorators_by_name(node, "parameter"):
            parameter_args = _get_decorator_spec(
                parameter_decorator,
                (
                    Argument("code", [ast.Constant]),
                    Argument("type", [ast.Name]),
                    Argument("name", [ast.Constant]),
                    Argument("choices", [ast.List]),
                    Argument("help", [ast.Constant]),
                    Argument("default", [ast.Constant, ast.List]),
                    Argument("widget", [ast.Attribute]),
                    Argument("connection", [ast.Constant]),
                    Argument("required", [ast.Constant], default_value=True),
                    Argument("multiple", [ast.Constant], default_value=False),
                ),
            )

            try:
                arg_type_name = parameter_args.pop("type")["value"]
                if arg_type_name not in TYPES_BY_PYTHON_TYPE:
                    raise InvalidParameterError(f"Unsupported parameter type: {arg_type_name}")

                type_class = TYPES_BY_PYTHON_TYPE[arg_type_name]()

                # Convert args spec to parameter kwargs
                param_kwargs = {k: v["value"] for k, v in parameter_args.items()}

                parameter = Parameter(type=type_class.expected_type, **param_kwargs)
                pipeline_parameters.append(parameter)

            except KeyError as e:
                raise InvalidParameterError(f"Missing required parameter attribute: {e}")

        validate_parameters(pipeline_parameters)

        # Create and return the pipeline
        return Pipeline(
            parameters=pipeline_parameters,
            function=None,
            name=pipeline_name,
            timeout=timeout,
        )

    # If we get here, no pipeline was found
    raise PipelineNotFound("No function with openhexa.sdk pipeline decorator found.")
