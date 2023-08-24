import ast
import base64
import dataclasses
import importlib
import io
import os
import sys
import typing
from zipfile import ZipFile

import requests
from .pipeline import Pipeline


class PipelineNotFound(Exception):
    pass


@dataclasses.dataclass
class PipelineParameterSpecs:
    code: str
    type: typing.Union[typing.Type[str], typing.Type[int], typing.Type[bool]]
    name: typing.Optional[str] = None
    choices: typing.Optional[typing.Sequence] = None
    help: typing.Optional[str] = None
    default: typing.Optional[typing.Any] = None
    required: bool = True
    multiple: bool = False


@dataclasses.dataclass
class PipelineSpecs:
    code: str
    name: str
    parameters: typing.Sequence[PipelineParameterSpecs] = None
    timeout: int = None


def import_pipeline(pipeline_dir_path: str):
    pipeline_dir = os.path.abspath(pipeline_dir_path)
    sys.path.append(pipeline_dir)
    pipeline_package = importlib.import_module("pipeline")

    pipeline = next(v for _, v in pipeline_package.__dict__.items() if v and type(v) == Pipeline)
    return pipeline


def get_openhexa_decorator_id(tree: ast.AST, decorator: str) -> str:
    """Retrieve an openhexa decorator id. This function help to find if a decorator has been imported
    from openhexa.sdk module and, if yes, return the decorator_id or alias.

    Parameters
    ----------
    tree : ast.AST
        Tree representing the pipeline code
    decorator : str
        An identifier for the decorator we're looking for.

    Returns
    -------
    str | None
        The decorator id or alias if found, else None.
    """
    openhexa_module_name = "openhexa.sdk"

    # First, we need to verify that openhexa.sdk.pipeline decorator is imported and is the one used for the pipeline node.
    for node in tree.body:
        # with import like 'from x import y as z' alias.name will be 'y' and alias.asname 'z'
        if isinstance(node, ast.ImportFrom) and node.module == openhexa_module_name:
            if any([alias.name == decorator for alias in node.names]):
                import_alias = [alias for alias in node.names if alias.name == decorator][0]
                return import_alias.asname if import_alias.asname else import_alias.name

            # for import 'from x import *' the decorator param passed to this function will be the decorator_id
            if len(node.names) == 1 and node.names[0].name == "*":
                return decorator

        if isinstance(node, ast.Import):
            # for simple import (e.g : import module) we only need to check if the module is present
            if any([alias.name == openhexa_module_name for alias in node.names]):
                import_alias = [alias for alias in node.names if alias.name == openhexa_module_name][0]
                return import_alias.asname if import_alias.asname else import_alias.name


def get_pipeline_node_specs(tree: ast.AST) -> (ast.AST, PipelineSpecs):
    pipeline_node = None
    pipeline_args = {}

    decorator_id = get_openhexa_decorator_id(tree, "pipeline")
    if not decorator_id:
        return None

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and any(
            [
                hasattr(dec, "func") and isinstance(dec.func, ast.Name) and dec.func.id == decorator_id
                for dec in node.decorator_list
            ]
        ):
            pipeline_node = node
            break

    if pipeline_node:
        pipeline_decorator = [dec for dec in pipeline_node.decorator_list if dec.func.id == decorator_id][0]
        for keyword in pipeline_decorator.keywords:
            # A keyword (keyword argument) can be of class ast.Constant or ast.Name
            # if it's an instance of ast.Name the value is hold by the id property
            pipeline_args[keyword.arg] = (
                keyword.value.value if isinstance(keyword.value, ast.Constant) else keyword.value.id
            )

        return pipeline_node, PipelineSpecs(code=pipeline_node.name, **pipeline_args)


def get_pipeline_parameters_specs(tree: ast.AST, pipeline_node: ast.AST) -> typing.Sequence[PipelineParameterSpecs]:
    decorator_id = get_openhexa_decorator_id(tree, "parameter")
    # we consider that the pipeline has no parameter
    if not decorator_id:
        return None

    param_decorators = [decorator for decorator in pipeline_node.decorator_list if decorator.func.id == decorator_id]
    params = []
    for param_decorator in param_decorators:
        param_decorator_args = {}
        for keyword in param_decorator.keywords:
            param_decorator_args[keyword.arg] = (
                keyword.value.value if isinstance(keyword.value, ast.Constant) else keyword.value.id
            )
        # param_decorator.args[0].value contains the @parameter decorator code
        param_specs = PipelineParameterSpecs(code=param_decorator.args[0].value, **param_decorator_args)
        params.append(param_specs)

    return params


def get_pipeline_specs(pipeline_content: str) -> PipelineSpecs:
    tree = ast.parse(pipeline_content)
    # In order to search for the pipeline decorator, we visit each node of the generated tree,
    # then check if a node of type function with id 'pipeline' (pipeline decorator) is present.
    pipeline_node_specs = get_pipeline_node_specs(tree)
    if not pipeline_node_specs:
        raise PipelineNotFound("No function with openhexa.sdk pipeline decorator found.")

    pipeline_node, pipeline_specs = pipeline_node_specs
    pipeline_parameter_specs = get_pipeline_parameters_specs(tree, pipeline_node)
    setattr(pipeline_specs, "parameters", pipeline_parameter_specs)

    return pipeline_specs


def download_pipeline(url: str, token: str, run_id: str, target_dir):
    r = requests.post(
        url + "/graphql/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "query": """
            query PipelineDownload($id: UUID!) {
              pipelineRun(id: $id) {
                id
                version {
                  number
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
