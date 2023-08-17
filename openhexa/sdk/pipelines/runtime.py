import ast
import base64
import importlib
import io
import os
import sys
import typing
from zipfile import ZipFile

import requests
from pathlib import Path
from .pipeline import Pipeline
from .utils import PipelineSpecs, PipelineParameterSpecs


def import_pipeline(pipeline_dir_path: str):
    pipeline_dir = os.path.abspath(pipeline_dir_path)
    sys.path.append(pipeline_dir)
    pipeline_package = importlib.import_module("pipeline")

    pipeline = next(v for _, v in pipeline_package.__dict__.items() if v and type(v) == Pipeline)
    return pipeline


def get_pipeline_specs(pipeline_dir_path) -> typing.Tuple[PipelineSpecs, typing.List[PipelineParameterSpecs]]:
    pipeline_dir = os.path.abspath(pipeline_dir_path)
    sys.path.append(pipeline_dir)
    pipeline_node = None

    with open(pipeline_dir_path / Path("pipeline.py")) as f:
        tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and [
                decorator for decorator in node.decorator_list if decorator.func and decorator.func.id == "pipeline"
            ]:
                pipeline_node = node
                break

    if pipeline_node:
        pipeline_decorator = [
            decorator for decorator in pipeline_node.decorator_list if decorator.func.id == "pipeline"
        ]
        pipeline_args = {}
        for keyword in pipeline_decorator[0].keywords:
            pipeline_args[keyword.arg] = (
                keyword.value.value if isinstance(keyword.value, ast.Constant) else keyword.value.id
            )

        pipeline_specs = PipelineSpecs(code=pipeline_node.name, **pipeline_args)

        param_decorators = [decorator for decorator in pipeline_node.decorator_list if decorator.func.id == "parameter"]
        params = []

        for param_decorator in param_decorators:
            param_decorator_args = {}
            for keyword in param_decorator.keywords:
                param_decorator_args[keyword.arg] = (
                    keyword.value.value if isinstance(keyword.value, ast.Constant) else keyword.value.id
                )
            param_specs = PipelineParameterSpecs(code=param_decorator.args[0].value, **param_decorator_args)
            params.append(param_specs)

        return pipeline_specs, params


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
