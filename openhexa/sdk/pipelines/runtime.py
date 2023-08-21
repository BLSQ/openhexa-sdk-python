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
from pathlib import Path
from .pipeline import Pipeline


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
    parameters: typing.Sequence[PipelineParameterSpecs]
    timeout: int = None


def import_pipeline(pipeline_dir_path: str):
    pipeline_dir = os.path.abspath(pipeline_dir_path)
    sys.path.append(pipeline_dir)
    pipeline_package = importlib.import_module("pipeline")

    pipeline = next(v for _, v in pipeline_package.__dict__.items() if v and type(v) == Pipeline)
    return pipeline


def get_pipeline_specs(pipeline_dir) -> PipelineSpecs:
    pipeline_node = None
    pipeline_decorator = None
    param_decorators = None

    with open(pipeline_dir / Path("pipeline.py")) as f:
        tree = ast.parse(f.read())
        # In order to search for the pipeline decorator, we visit each node of the generated tree,
        # then check if a node of type function with id 'pipeline' (pipeline decorator) is present.
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and any(
                [hasattr(dec, "func") and dec.func.id == "pipeline" for dec in node.decorator_list]
            ):
                # retrieve the @pipeline decorator and parameter(s) if present.
                pipeline_node = node
                pipeline_decorator = [dec for dec in node.decorator_list if dec.func.id == "pipeline"][0]
                param_decorators = [
                    decorator for decorator in pipeline_node.decorator_list if decorator.func.id == "parameter"
                ]

    if not pipeline_node:
        raise Exception("Pipeline function not found. Check that openhexa.sdk pipeline decorator is present.")

    pipeline_args = {}
    for keyword in pipeline_decorator.keywords:
        # A keyword (keyword argument) can be of class ast.Constant or ast.Name
        # if it's an instance of ast.Name the value is hold by the id property
        pipeline_args[keyword.arg] = (
            keyword.value.value if isinstance(keyword.value, ast.Constant) else keyword.value.id
        )
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

    return PipelineSpecs(code=pipeline_node.name, parameters=params, **pipeline_args)


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
