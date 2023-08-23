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


def _get_openhexa_decorator_id(tree: ast.AST, decorator: str):
    imported_nodes = [node for node in tree.body if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom)]
    if not imported_nodes:
        return None

    decorator_id = None
    # First, we need to verify that openhexa.sdk.pipeline decorator is imported and is the one used for the pipeline node.
    for import_node in imported_nodes:
        # with import like 'from x import y as z' alias.name will y and alias.asname z
        if (
            isinstance(import_node, ast.ImportFrom)
            and import_node.module == "openhexa.sdk"
            and any([alias.name == decorator for alias in import_node.names])
        ):
            import_alias = [alias for alias in import_node.names if alias.name == decorator][0]
            decorator_id = import_alias.asname if import_alias.asname else import_alias.name
            break

        # for simple import (e.g : import module) we only need to check if the module is present
        if isinstance(import_node, ast.Import) and any([alias.name == "openhexa.sdk" for alias in import_node.names]):
            import_alias = [alias for alias in import_node.names if alias.name == "openhexa.sdk"][0]
            decorator_id = import_alias.asname if import_alias.asname else import_alias.name
            break

    return decorator_id


def _get_pipeline_node_specs(tree: ast.AST) -> (ast.AST, PipelineSpecs):
    pipeline_node = None
    pipeline_args = {}

    decorator_id = _get_openhexa_decorator_id(tree, "pipeline")
    if not decorator_id:
        return None

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and any(
            [hasattr(dec, "func") and dec.func.id == decorator_id for dec in node.decorator_list]
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


def _get_pipeline_parameters_specs(tree: ast.AST, pipeline_node: ast.AST) -> typing.Sequence[PipelineParameterSpecs]:
    decorator_id = _get_openhexa_decorator_id(tree, "parameter")
    # we assume that the pipeline has no parameter
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
    pipeline_node_specs = _get_pipeline_node_specs(tree)
    if not pipeline_node_specs:
        raise PipelineNotFound("No function with openhexa.sdk pipeline decorator found.")

    pipeline_node, pipeline_specs = pipeline_node_specs
    pipeline_parameter_specs = _get_pipeline_parameters_specs(tree, pipeline_node)
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
