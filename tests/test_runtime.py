from dataclasses import asdict
from openhexa.sdk.pipelines.runtime import get_pipeline_specs
from pathlib import Path
from unittest import TestCase

FIXTURES_DIR = "tests/fixtures"


def test_get_pipeline_simple_pipeline_specs():
    pipeline_code = "simple_pipeline"
    pipeline_dir = Path.cwd() / FIXTURES_DIR / pipeline_code

    pipeline_specs = get_pipeline_specs(pipeline_dir)

    assert len(pipeline_specs.parameters) == 0
    assert pipeline_specs.code == pipeline_code
    assert pipeline_specs.name == pipeline_code
    assert pipeline_specs.timeout is None


def test_get_pipeline_with_parameters_specs():
    test_case = TestCase()
    pipeline_code = "pipeline_with_parameters"
    pipeline_dir = Path.cwd() / FIXTURES_DIR / pipeline_code
    pipeline_specs = get_pipeline_specs(pipeline_dir)

    assert pipeline_specs.code == pipeline_code
    assert pipeline_specs.name == pipeline_code
    assert pipeline_specs.timeout == 5000

    assert len(pipeline_specs.parameters) == 3

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
