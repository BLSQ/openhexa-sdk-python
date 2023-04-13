from unittest.mock import Mock

import pytest

from openhexa.sdk.pipelines.arguments import Argument, ArgumentValueError
from openhexa.sdk.pipelines.pipeline import Pipeline


def test_pipeline_run_valid_config():
    pipeline_func = Mock()
    argument_1 = Argument("arg1", type=str)
    argument_2 = Argument("arg2", type=str, multiple=True)
    argument_3 = Argument("arg3", type=int, default=33)
    pipeline = Pipeline("code", pipeline_func, [argument_1, argument_2, argument_3])
    pipeline.run({"arg1": "ab", "arg2": ["cd", "ef"]})

    pipeline_func.assert_called_once_with(arg1="ab", arg2=["cd", "ef"], arg3=33)


def test_pipeline_run_invalid_config():
    pipeline_func = Mock()
    argument_1 = Argument("arg1", type=str)
    pipeline = Pipeline("code", pipeline_func, [argument_1])
    with pytest.raises(ArgumentValueError):
        pipeline.run({"arg1": 3})


def test_pipeline_run_extra_config():
    pipeline_func = Mock()
    argument_1 = Argument("arg1", type=str)
    pipeline = Pipeline("code", pipeline_func, [argument_1])
    with pytest.raises(ArgumentValueError):
        pipeline.run({"arg1": "ok", "arg2": "extra"})


def test_pipeline_parameters_specs():
    pipeline_func = Mock()
    argument_1 = Argument("arg1", type=str)
    argument_2 = Argument("arg2", type=str, multiple=True)
    pipeline = Pipeline("code", pipeline_func, [argument_1, argument_2, argument_2])

    assert pipeline.parameters_specs() == {
        "arg1": {
            "code": "arg1",
            "name": None,
            "type": "str",
            "required": True,
            "choices": None,
            "help": None,
            "multiple": False,
            "default": None,
        },
        "arg2": {
            "code": "arg2",
            "name": None,
            "type": "str",
            "required": True,
            "choices": None,
            "help": None,
            "multiple": True,
            "default": None,
        },
    }
