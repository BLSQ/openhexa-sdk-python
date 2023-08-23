import pytest

from dataclasses import asdict
from openhexa.sdk.pipelines.runtime import get_pipeline_specs, PipelineNotFound
from unittest import TestCase


def test_get_pipeline_simple_pipeline_specs():
    pipeline_code = """
from openhexa.sdk import current_run, pipeline

@pipeline("simple_pipeline", name="simple_pipeline")
def simple_pipeline():
    count = task_1()
    task_2(count)

@simple_pipeline.task
def task_1():
    current_run.log_info("In task 1...")
    return 42

@simple_pipeline.task
def task_2(count):
    current_run.log_info(f"In task 2... count is {count}")

if __name__ == "__main__":
    simple_pipeline()
"""

    pipeline_specs = get_pipeline_specs(pipeline_code)

    assert pipeline_specs.code == pipeline_specs.code
    assert pipeline_specs.name == pipeline_specs.name
    assert pipeline_specs.timeout is None
    assert pipeline_specs.parameters is None


def test_get_pipeline_with_parameters_specs():
    pipeline_code = """
from openhexa.sdk import current_run, pipeline, parameter


@pipeline("pipeline_with_parameters", name="pipeline_with_parameters", timeout=5000)
@parameter(
    "param1",
    name="First parameter",
    type=str,
)
@parameter(
    "param2",
    type=str,
    multiple=True,
    help="This is the second parameter",
)
@parameter("param3", name="Third parameter", type=int, default=2)
def pipeline_with_parameters(param1: str, param2: str, param3: int):
    count = task_1(param1=param3)
    task_2(param2)
    task_3(count)


@pipeline_with_parameters.task
def task_1(param):
    current_run.log_info("In task 1...")

    return param + 1


@pipeline_with_parameters.task
def task_2(param):
    current_run.log_info(f"In task 2... param :  {param}")


@pipeline_with_parameters.task
def task_3(param):
    current_run.log_info(f"In task 3... param :  {param}")


if __name__ == "__main__":
    pipeline_with_parameters()
"""
    pipeline_specs = get_pipeline_specs(pipeline_code)

    assert pipeline_specs.code == pipeline_specs.code
    assert pipeline_specs.name == pipeline_specs.name
    assert pipeline_specs.timeout == 5000
    assert len(pipeline_specs.parameters) == 3
    test_case = TestCase()

    parameters = [asdict(spec) for spec in pipeline_specs.parameters]
    test_case.assertEqual(
        parameters,
        [
            {
                "code": "param1",
                "type": "str",
                "name": "First parameter",
                "choices": None,
                "help": None,
                "default": None,
                "required": True,
                "multiple": False,
            },
            {
                "code": "param2",
                "type": "str",
                "name": None,
                "choices": None,
                "help": "This is the second parameter",
                "default": None,
                "required": True,
                "multiple": True,
            },
            {
                "code": "param3",
                "type": "int",
                "name": "Third parameter",
                "choices": None,
                "help": None,
                "default": 2,
                "required": True,
                "multiple": False,
            },
        ],
    )


def test_get_pipeline_specs_not_found():
    pipeline_code = """
from openhexa.sdk import current_run, pipeline as sdk_pipeline, parameter as param


@pipeline("pipeline_with_parameters", name="pipeline_with_parameters", timeout=5000)
@parameter(
    "param1",
    name="First parameter",
    type=str,
)
@parameter(
    "param2",
    type=str,
    multiple=True,
    help="This is the second parameter",
)
@parameter("param3", name="Third parameter", type=int, default=2)
def pipeline_with_parameters(param1: str, param2: str, param3: int):
    count = task_1(param1=param3)
    task_2(param2)
    task_3(count)


@pipeline_with_parameters.task
def task_1(param):
    current_run.log_info("In task 1...")

    return param + 1


@pipeline_with_parameters.task
def task_2(param):
    current_run.log_info(f"In task 2... param :  {param}")


@pipeline_with_parameters.task
def task_3(param):
    current_run.log_info(f"In task 3... param :  {param}")


if __name__ == "__main__":
    pipeline_with_parameters()
"""

    with pytest.raises(PipelineNotFound):
        get_pipeline_specs(pipeline_code)


def test_get_pipeline_and_parameters_specs_with_alias():
    pipeline_code = """
from openhexa.sdk import current_run, pipeline as sdk_pipeline, parameter as param


@sdk_pipeline("pipeline_with_parameters", name="pipeline_with_parameters", timeout=5000)
@param(
    "param1",
    name="First parameter",
    type=str,
)
@param(
    "param2",
    type=str,
    multiple=True,
    help="This is the second parameter",
)
@param("param3", name="Third parameter", type=int, default=2)
def pipeline_with_parameters(param1: str, param2: str, param3: int):
    count = task_1(param1=param3)
    task_2(param2)
    task_3(count)


@pipeline_with_parameters.task
def task_1(param):
    current_run.log_info("In task 1...")

    return param + 1


@pipeline_with_parameters.task
def task_2(param):
    current_run.log_info(f"In task 2... param :  {param}")


@pipeline_with_parameters.task
def task_3(param):
    current_run.log_info(f"In task 3... param :  {param}")


if __name__ == "__main__":
    pipeline_with_parameters()
"""

    test_case = TestCase()
    pipeline_specs = get_pipeline_specs(pipeline_code)

    assert pipeline_specs.code == pipeline_specs.code
    assert pipeline_specs.name == pipeline_specs.name

    parameters = [asdict(spec) for spec in pipeline_specs.parameters]
    test_case.assertEqual(
        parameters,
        [
            {
                "code": "param1",
                "type": "str",
                "name": "First parameter",
                "choices": None,
                "help": None,
                "default": None,
                "required": True,
                "multiple": False,
            },
            {
                "code": "param2",
                "type": "str",
                "name": None,
                "choices": None,
                "help": "This is the second parameter",
                "default": None,
                "required": True,
                "multiple": True,
            },
            {
                "code": "param3",
                "type": "int",
                "name": "Third parameter",
                "choices": None,
                "help": None,
                "default": 2,
                "required": True,
                "multiple": False,
            },
        ],
    )
