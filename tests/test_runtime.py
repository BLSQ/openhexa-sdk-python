import typing

from unittest import TestCase
from pathlib import Path

from openhexa.sdk.pipelines.runtime import (
    get_pipeline_specs,
    PipelineNotFound,
)

FIXTURES_DIR = "tests/fixtures"

STRATEGIES: typing.List[typing.Literal["import", "ast"]] = ["import", "ast"]


class RuntimeTest(TestCase):
    def test_get_simple_pipeline_specs(self):
        pipeline_directory = Path.cwd() / f"{FIXTURES_DIR}/simple_pipeline"
        for strategy in STRATEGIES:
            pipeline_specs = get_pipeline_specs(pipeline_directory, strategy)

            assert pipeline_specs.code == "simple_pipeline"
            assert pipeline_specs.name == "simple_pipeline"
            assert pipeline_specs.timeout is None
            assert len(pipeline_specs.parameters) == 0

    def test_get_pipeline_with_parameters_specs(self):
        pipeline_directory = Path.cwd() / f"{FIXTURES_DIR}/pipeline_with_parameters"
        for strategy in STRATEGIES:
            pipeline_specs = get_pipeline_specs(pipeline_directory, strategy)

            assert pipeline_specs.code == pipeline_specs.code
            assert pipeline_specs.name == pipeline_specs.name
            assert pipeline_specs.timeout == 5000
            assert len(pipeline_specs.parameters) == 3

            parameters_as_dict = pipeline_specs.parameters_as_dict()
            assert parameters_as_dict == [
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
            ]

    def test_get_pipeline_specs_alias_errors(self):
        pipeline_directory = Path.cwd() / f"{FIXTURES_DIR}/pipeline_with_alias_errors"
        for strategy in STRATEGIES:
            with self.assertRaises(PipelineNotFound):
                get_pipeline_specs(pipeline_directory, strategy)

    def test_get_pipeline_specs_alias_correct(self):
        pipeline_directory = Path.cwd() / f"{FIXTURES_DIR}/pipeline_with_alias_correct"
        for strategy in STRATEGIES:
            pipeline_specs = get_pipeline_specs(pipeline_directory, strategy)

            assert pipeline_specs.code == pipeline_specs.code
            assert pipeline_specs.name == pipeline_specs.name

            parameters = pipeline_specs.parameters_as_dict()
            self.assertEqual(
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

    def test_get_pipeline_and_parameters_specs_wildcard_import(self):
        pipeline_directory = Path.cwd() / f"{FIXTURES_DIR}/pipeline_with_wildcard_imports"
        for strategy in STRATEGIES:
            pipeline_specs = get_pipeline_specs(pipeline_directory, strategy)

            assert pipeline_specs.code == pipeline_specs.code
            assert pipeline_specs.name == pipeline_specs.name

            parameters = pipeline_specs.parameters_as_dict()
            self.assertEqual(
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
