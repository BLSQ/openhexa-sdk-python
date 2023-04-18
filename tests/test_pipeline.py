from unittest.mock import Mock

import pytest

from openhexa.sdk.pipelines.parameter import Parameter, ParameterValueError
from openhexa.sdk.pipelines.pipeline import Pipeline


def test_pipeline_run_valid_config():
    pipeline_func = Mock()
    parameter_1 = Parameter("arg1", type=str)
    parameter_2 = Parameter("arg2", type=str, multiple=True)
    parameter_3 = Parameter("arg3", type=int, default=33)
    pipeline = Pipeline(
        "code", "pipeline", pipeline_func, [parameter_1, parameter_2, parameter_3]
    )
    pipeline.run({"arg1": "ab", "arg2": ["cd", "ef"]})

    assert pipeline.name == "pipeline"
    pipeline_func.assert_called_once_with(arg1="ab", arg2=["cd", "ef"], arg3=33)


def test_pipeline_run_invalid_config():
    pipeline_func = Mock()
    parameter_1 = Parameter("arg1", type=str)
    pipeline = Pipeline("code", "pipeline", pipeline_func, [parameter_1])
    with pytest.raises(ParameterValueError):
        pipeline.run({"arg1": 3})


def test_pipeline_run_extra_config():
    pipeline_func = Mock()
    parameter_1 = Parameter("arg1", type=str)
    pipeline = Pipeline("code", "pipeline", pipeline_func, [parameter_1])
    with pytest.raises(ParameterValueError):
        pipeline.run({"arg1": "ok", "arg2": "extra"})


def test_pipeline_parameters_spec():
    pipeline_func = Mock()
    parameter_1 = Parameter("arg1", type=str)
    parameter_2 = Parameter("arg2", type=str, multiple=True)
    pipeline = Pipeline("code", "pipeline", pipeline_func, [parameter_1, parameter_2])

    assert pipeline.parameters_spec() == [
        {
            "code": "arg1",
            "name": None,
            "type": "str",
            "required": True,
            "choices": None,
            "help": None,
            "multiple": False,
            "default": None,
        },
        {
            "code": "arg2",
            "name": None,
            "type": "str",
            "required": True,
            "choices": None,
            "help": None,
            "multiple": True,
            "default": None,
        },
    ]
