from unittest.mock import Mock

import pytest

from openhexa.sdk.pipelines.parameter import Parameter, ParameterValueError
from openhexa.sdk.pipelines.pipeline import Pipeline, PipelineSpecs


def test_pipeline_run_valid_config():
    pipeline_func = Mock()
    parameter_1 = Parameter("arg1", type=str)
    parameter_2 = Parameter("arg2", type=str, multiple=True)
    parameter_3 = Parameter("arg3", type=int, default=33)
    pipeline = Pipeline("code", "pipeline", pipeline_func, [parameter_1, parameter_2, parameter_3])
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


def test_pipeline_to_specs():
    pipeline_func = Mock()
    parameter_1 = Parameter("arg1", type=str)
    parameter_2 = Parameter("arg2", type=str, multiple=True)
    pipeline = Pipeline("code", "pipeline", pipeline_func, [parameter_1, parameter_2])

    pipeline_specs = pipeline.to_specs()
    assert isinstance(pipeline_specs, PipelineSpecs)
    assert pipeline_specs.code == pipeline.code
    assert pipeline_specs.name == pipeline.name
    assert pipeline_specs.timeout == pipeline.timeout

    assert len(pipeline_specs.parameters) == 2
