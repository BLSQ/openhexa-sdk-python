import ast
import base64
import dataclasses
import io
import importlib

import os
import requests
import sys
import typing

from zipfile import ZipFile
from pathlib import Path
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
    parameters: typing.Sequence[PipelineParameterSpecs] = dataclasses.field(default_factory=list)
    timeout: int = None


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

    # First, we need to verify that openhexa.sdk.pipeline decorator is imported and is the one used for the pipeline node.
    for node in tree.body:
        if not isinstance(node, ast.ImportFrom) or node.module != "openhexa.sdk":
            # We only check imports from openhexa.sdk module
            continue

        # We try to find the pipeline decorator in the import list
        # as an alias (from openhexa.sdk import pipeline as sdk_pipeline) or as a name (from openhexa.sdk import pipeline)
        for alias in node.names:
            if alias.name == decorator:
                return alias.asname if alias.asname else alias.name

        # If the pipeline decorator is not found in the import list, we check if it's imported as a wildcard
        if "*" in [x.name for x in node.names]:
            return decorator

    # We did not find the decorator in the imports
    return None


def get_pipeline_node_specs(tree: ast.AST) -> (ast.AST, PipelineSpecs):
    pipeline_node = None
    pipeline_args = {}

    decorator_id = get_openhexa_decorator_id(tree, "pipeline")
    if not decorator_id:
        raise PipelineNotFound("'@pipeline' not found")

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # We check if the function has a pipeline decorator
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Call) and decorator.func.id == decorator_id:
                    # args[0] contains pipeline code
                    pipeline_code = decorator.args[0].value
                    pipeline_node = node
                    break

    if not pipeline_node:
        raise PipelineNotFound("No function with openhexa.sdk pipeline decorator found.")

    pipeline_decorator = [dec for dec in pipeline_node.decorator_list if dec.func.id == decorator_id][0]
    for keyword in pipeline_decorator.keywords:
        # A keyword (keyword argument) can be of class ast.Constant or ast.Name
        # if it's an instance of ast.Name the value is hold by the id property
        pipeline_args[keyword.arg] = (
            keyword.value.value if isinstance(keyword.value, ast.Constant) else keyword.value.id
        )
    return pipeline_node, PipelineSpecs(code=pipeline_code, **pipeline_args)


def get_pipeline_parameters_specs(tree: ast.AST, pipeline_node: ast.AST) -> typing.Sequence[PipelineParameterSpecs]:
    params = []
    parameter_decorator_id = get_openhexa_decorator_id(tree, "parameter")
    if not parameter_decorator_id:
        # No parameter decorator found
        return params

    for decorator in pipeline_node.decorator_list:
        if decorator.func.id != parameter_decorator_id:
            # We skip decorators that are not parameter decorators
            continue

        param_decorator_args = {}
        for keyword in decorator.keywords:
            param_decorator_args[keyword.arg] = (
                keyword.value.value if isinstance(keyword.value, ast.Constant) else keyword.value.id
            )
        # param_decorator.args[0].value contains the @parameter decorator code
        param_specs = PipelineParameterSpecs(code=decorator.args[0].value, **param_decorator_args)
        params.append(param_specs)

    return params


def get_pipeline_specs(
    filepath_or_buffer: typing.Union[str, typing.TextIO, Path], strategy: typing.Literal["import", "ast"]
) -> PipelineSpecs:
    if strategy == "ast":
        return _get_pipeline_specs_with_ast(filepath_or_buffer)
    elif strategy == "import":
        return _get_pipeline_specs_with_import(filepath_or_buffer)
    else:
        raise ValueError(f"Invalid strategy {strategy}")


def _get_pipeline_specs_with_ast(filepath_or_buffer: typing.Union[str, typing.TextIO]) -> PipelineSpecs:
    # TODO: filepath_or_buffer can be either 'some_dir/pipeline.py', the result of open(), or StringIO...
    tree = ast.parse(filepath_or_buffer)
    # In order to search for the pipeline decorator, we visit each node of the generated tree,
    # then check if a node of type function with id 'pipeline' (pipeline decorator) is present.
    pipeline_node, specs = get_pipeline_node_specs(tree)
    specs.parameters = get_pipeline_parameters_specs(tree, pipeline_node)

    return specs


def _get_pipeline_specs_with_import(filepath_or_buffer: typing.Union[str, typing.TextIO]) -> PipelineSpecs:
    # TODO: filepath_or_buffer can be either 'some_dir/pipeline.py', the result of open(), or StringIO...
    # TODO: not sure how it would work with a buffer... create a temporary file?
    pipeline_dir = os.path.abspath(filepath_or_buffer)
    sys.path.append(pipeline_dir)
    pipeline_package = importlib.import_module("pipeline")
    pipeline = next(v for _, v in pipeline_package.__dict__.items() if v and type(v) == Pipeline)
    specs = PipelineSpecs(code=pipeline.code, name=pipeline.name)
    # TODO: continue building specs

    return specs


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
