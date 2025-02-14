"""Utilities used by containerized pipeline runners to import and download pipelines."""

import ast
import base64
import importlib
import io
import os
import string
import sys
import typing
from dataclasses import dataclass, field
from pathlib import Path
from zipfile import ZipFile

import requests

from openhexa.sdk.pipelines.exceptions import PipelineNotFound
from openhexa.sdk.pipelines.parameter import TYPES_BY_PYTHON_TYPE, Parameter, validate_parameters_with_connection

from .pipeline import Pipeline


@dataclass
class Argument:
    """Argument of a decorator."""

    name: string
    types: list[typing.Any] = field(default_factory=list)
    default_value: typing.Any = None


def import_pipeline(pipeline_dir_path: str):
    """Import pipeline code within provided path using importlib."""
    pipeline_dir = os.path.abspath(pipeline_dir_path)
    sys.path.append(pipeline_dir)
    pipeline_package = importlib.import_module("pipeline")

    pipeline = next(v for _, v in pipeline_package.__dict__.items() if v and type(v) == Pipeline)
    return pipeline


def download_pipeline(url: str, token: str, run_id: str, target_dir: str):
    """Download pipeline code and unzip it into the target directory."""
    r = requests.post(
        url + "/graphql/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "query": """
            query PipelineDownload($id: UUID!) {
              pipelineRun(id: $id) {
                id
                version {
                  versionNumber
                }
                code
              }
            }
            """,
            "variables": {"id": run_id},
        },
        timeout=30,
    )
    r.raise_for_status()
    data = r.json()
    zipfile = base64.b64decode(data["data"]["pipelineRun"]["code"].encode("ascii"))
    source_dir = os.getcwd()
    os.chdir(target_dir)
    with ZipFile(io.BytesIO(zipfile)) as zf:
        zf.extractall()
    os.chdir(source_dir)


def _get_decorators_by_name(node, name):
    return [dec for dec in node.decorator_list if isinstance(dec, ast.Call) and dec.func.id == name]


def _get_decorator_arg_value(decorator, arg: Argument, index: int):
    for keyword in decorator.keywords:
        if keyword.arg == arg.name:
            if type(keyword.value) not in arg.types:
                raise ValueError(
                    f"Unsupported argument type for {arg.name}: {type(keyword.value)}. Expected {arg.types}"
                )
            if isinstance(keyword.value, ast.Constant):
                return keyword.value.value
            elif isinstance(keyword.value, ast.Name):
                return keyword.value.id
            elif isinstance(keyword.value, ast.List):
                return [el.value for el in keyword.value.elts]
    try:
        return decorator.args[index].value
    except IndexError:
        return arg.default_value


def _get_decorator_spec(decorator, args: tuple[Argument]):
    d = {"name": decorator.func.id, "args": {}}

    for i, arg in enumerate(args):
        d["args"][arg.name] = _get_decorator_arg_value(decorator, arg, i)

    return d


def get_pipeline(pipeline_path: Path) -> Pipeline:
    """Return the pipeline with metadata and parameters from the pipeline code.

    Args:
        pipeline_path (Path): Path to the pipeline directory

    Raises
    ------
        PipelineNotFound: If no function with openhexa.sdk pipeline decorator is found.
        InvalidParameterError: If the parameter type is invalid/unknown.
        ValueError: If the value of an argument is not a primitive type.

    Returns
    -------
        Pipeline: The pipeline object with parameters and metadata.
    """
    tree = ast.parse(open(Path(pipeline_path) / "pipeline.py").read())
    pipeline = None
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue
        try:
            pipeline_decorator = _get_decorators_by_name(node, "pipeline")[0]
        except IndexError:
            continue
        else:
            pipeline_decorator_spec = _get_decorator_spec(
                pipeline_decorator,
                (
                    Argument("code", [ast.Constant]),
                    Argument("name", [ast.Constant]),
                    Argument("timeout", [ast.Constant]),
                ),
            )
            pipelines_parameters = []
            for parameter_decorator in _get_decorators_by_name(node, "parameter"):
                param_decorator_spec = _get_decorator_spec(
                    parameter_decorator,
                    (
                        Argument("code", [ast.Constant]),
                        Argument("type", [ast.Name]),
                        Argument("name", [ast.Constant]),
                        Argument("choices", [ast.List]),
                        Argument("help", [ast.Constant]),
                        Argument("default", [ast.Constant, ast.List]),
                        Argument("widget", [ast.Constant]),
                        Argument("connection", [ast.Constant]),
                        Argument("required", [ast.Constant], default_value=True),
                        Argument("multiple", [ast.Constant], default_value=False),
                    ),
                )
                parameter_args = param_decorator_spec["args"]
                try:
                    type_class = TYPES_BY_PYTHON_TYPE[parameter_args.pop("type")]()
                except KeyError:
                    raise ValueError(f"Unsupported parameter type: {parameter_args['type']}")
                parameter = Parameter(type=type_class.expected_type, **parameter_args)
                pipelines_parameters.append(parameter)

            validate_parameters_with_connection(pipelines_parameters)

            pipeline = Pipeline(parameters=pipelines_parameters, function=None, **pipeline_decorator_spec["args"])

    if pipeline is None:
        raise PipelineNotFound("No function with openhexa.sdk pipeline decorator found.")
    return pipeline
