"""Main pipeline module containing the building blocks for OpenHEXA pipelines.

See https://github.com/BLSQ/openhexa/wiki/User-manual#using-pipelines and
https://github.com/BLSQ/openhexa/wiki/Writing-OpenHEXA-pipelines for more information about OpenHEXA pipelines.
"""

import argparse
import datetime
import json
import os
import sys
import time
import typing
from logging import getLogger
from pathlib import Path

import requests
from multiprocess import get_context  # NOQA

from openhexa.sdk.utils import Environment, Settings, get_environment

from .parameter import FunctionWithParameter, Parameter, ParameterValueError
from .task import PipelineWithTask, Task
from .utils import get_local_workspace_config

logger = getLogger(__name__)


class Pipeline:
    """OpenHEXA pipeline class.

    Pipeline are usually instantiated through the @pipeline decorator.

    Attributes
    ----------
    name : str
        A user-friendly name for the pipeline (will be displayed in the web interface).
    function: typing.Callable
        The actual pipeline function.
    parameters : typing.Sequence[Parameter]
        A list of Parameter instance corresponding to the pipeline parameters.
    timeout : int
        The timeout in seconds after which the pipeline will be killed.
    """

    def __init__(
        self,
        name: str,
        function: typing.Callable,
        parameters: typing.Sequence[Parameter],
        timeout: int = None,
    ):
        self.name = name
        self.function = function
        self.parameters = parameters
        self.timeout = timeout
        self.tasks = []

    def task(self, function) -> PipelineWithTask:
        """Task decorator.

        Examples
        --------
        >>> @pipeline("my-pipeline")
        ... def my_pipeline():
        ...     result_1 = task1()
        ...     task2(result_1)
        ...
        ... @my_pipeline.task
        ... def task_1() -> int:
        ...     return 42
        ...
        ... @my_pipeline.task
        ... def task_2(foo: int):
        ...     pass
        """
        return PipelineWithTask(function, self)

    def run(self, config: dict[str, typing.Any]):
        """Run the pipeline using the provided config.

        Parameters
        ----------
        config : typing.Dict[str, typing.Any]
            The parameter values to use for this pipeline run.
        """
        now = datetime.datetime.now(tz=datetime.UTC).replace(microsecond=0).isoformat()
        print(f'{now} Starting pipeline "{self.name}"')

        # Validate / default parameters
        validated_config = {}
        for parameter in self.parameters:
            value = config.pop(parameter.code, None)
            validated_value = parameter.validate(value)
            validated_config[parameter.code] = validated_value

        if len(config) > 0:
            raise ParameterValueError(f"The provided config contains invalid key(s): {', '.join(list(config.keys()))}")

        self.function(**validated_config)

        # managing variables
        result_list = []
        context = get_context("spawn")
        pool = context.Pool()  # FIXME: set max size of pool
        total = len(self.tasks)
        completed = 0

        while True:
            tasks = self._get_available_tasks()
            # filter already pooled task, even if they are not finished
            tasks = [t for t in tasks if not t.pooled]

            if len(tasks) == 0 and len(result_list) == 0:
                # nothing running, nothing to do
                break

            for task in tasks:
                now = datetime.datetime.now(tz=datetime.UTC).replace(microsecond=0).isoformat()
                print(f'{now} Started task "{task.compute.__name__}"')
                result = pool.apply_async(task.run)
                result_list.append((result, task))
                task.pooled = True

            while True:
                dag_step = False

                for result, task in result_list:
                    if not result.ready():
                        continue
                    now = datetime.datetime.now(tz=datetime.UTC).replace(microsecond=0).isoformat()

                    completed += 1
                    progress = int(completed / total * 100)
                    print(f'{now} Finished task "{task.compute.__name__}"')
                    self._update_progress(progress)

                    try:
                        task_com_result = result.get()
                        task.result = task_com_result.result
                        task.start_time = task_com_result.start_time
                        task.end_time = task_com_result.end_time
                        dag_step = True
                    except Exception as e:  # NOQA
                        raise PipelineRunError(f"Pipeline {self.name} failed: {e}")

                if dag_step:
                    # remove finished tasks
                    result_list = [(r, t) for r, t in result_list if t.end_time is None]
                    break
                else:
                    # busy loop
                    time.sleep(0.3)

        pool.close()
        pool.join()

        now = datetime.datetime.now(tz=datetime.UTC).replace(microsecond=0).isoformat()
        print(f'{now} Successfully completed pipeline "{self.name}"')

    def to_dict(self):
        """Return a dictionary representation of the pipeline."""
        return {
            "name": self.name,
            "parameters": [p.to_dict() for p in self.parameters],
            "timeout": self.timeout,
            "function": self.function.__dict__ if self.function else None,
            "tasks": [t.__dict__ for t in self.tasks],
        }

    def _get_available_tasks(self) -> list[Task]:
        return [task for task in self.tasks if task.is_ready()]

    def _update_progress(self, progress: int):
        if self._connected:
            token = os.environ["HEXA_TOKEN"]
            headers = {"Authorization": "Bearer %s" % token}
            query = """
                            mutation updatePipelineProgress ($input: UpdatePipelineProgressInput!) {
                                updatePipelineProgress(input: $input) { success errors }
                            }"""
            r = requests.post(
                f"{os.environ['HEXA_SERVER_URL']}/graphql/",
                headers=headers,
                json={
                    "query": query,
                    "variables": {"input": {"percent": progress}},
                },
                verify=Settings.verify_ssl(),
            )
            r.raise_for_status()
        else:
            print(f"Progress update: {progress}%")

    @property
    def _connected(self) -> bool:
        env = get_environment()

        return env == Environment.CLOUD_PIPELINE and "HEXA_SERVER_URL" in os.environ

    def __call__(self, config: dict[str | typing.Any] | None = None):
        """Call the pipeline by running it, after having configured the environment.

        This method can be called with an explicit configuration. If no configuration is provided, it will parse the
        command-line arguments to build it.
        """
        # User can run their pipeline using `python pipeline.py`. It's considered as a standalone usage of the library.
        # Since we still support this use case for the moment, we'll try to load the workspace.yaml
        # at the path of the file
        if get_environment() == Environment.STANDALONE:
            os.environ.update(get_local_workspace_config(Path(sys.argv[0]).parent))

        if config is None:  # Called without arguments, in the pipeline file itself
            parser = argparse.ArgumentParser(exit_on_error=False)
            parser.add_argument("-c", "--config")
            parser.add_argument("-f", "--config-file")
            # We can't use parse_args, as it will call sys.exit() if there are unrecognized arguments
            args, argv = parser.parse_known_args()
            if argv or (args.config_file is not None and args.config is not None):
                raise ValueError(
                    f"Unrecognized arguments: {' '.join(argv)}. Running a pipeline requires a single "
                    "argument: either an inline JSON config with the --config/-c argument, or a JSON "
                    "config file with the --config-file/-f argument."
                )
            if args.config_file is not None:
                with open(args.config_file) as cf:
                    try:
                        config = json.load(cf)
                    except json.JSONDecodeError:
                        raise PipelineConfigError("The provided config is not valid JSON")

            elif args.config is not None:
                try:
                    config = json.loads(args.config)
                except json.JSONDecodeError:
                    raise PipelineConfigError("The provided config is not valid JSON")
            else:
                config = {}

        self.run(config)


def pipeline(
    code: str = None, name: str = None, timeout: int = None
) -> typing.Callable[[typing.Callable[..., typing.Any]], Pipeline]:
    """Decorate a Python function as an OpenHEXA pipeline.

    Parameters
    ----------
    code : str, optional
        Deprecated identifier for the pipeline. A unique identifier will be auto-generated.
    name : str
        A name for the pipeline (will be shown in the web interface).
    timeout : int, optional
        An optional timeout, in seconds, after which the pipeline run will be terminated (if not provided, a default
        timeout will be applied by the OpenHEXA backend)

    Returns
    -------
    typing.Callable
        A decorator that returns a Pipeline

    Examples
    --------
    >>> @pipeline("my-pipeline")
    ... def my_pipeline():
    ...     a_task()
    ...
    ... @my_pipeline.task
    ... def a_task() -> int:
    ...     return 42
    """
    name = name or code

    def decorator(fun):
        if isinstance(fun, FunctionWithParameter):
            parameters = fun.get_all_parameters()
        else:
            parameters = []

        return Pipeline(name, fun, parameters, timeout)

    return decorator


class PipelineConfigError(Exception):
    """Error raised whenver the config passed to the pipeline run method is invalid."""

    pass


class PipelineRunError(Exception):
    """Generic pipeline runtime error, raised whenever user code raises an exception."""

    pass
