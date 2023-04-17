from __future__ import annotations

import argparse
import datetime
import json
import string
import time
import typing
from logging import getLogger

from multiprocess import get_context

from .parameter import FunctionWithParameter, Parameter, ParameterValueError
from .task import PipelineWithTask

logger = getLogger(__name__)


def pipeline(
    code: str, *, name: str = None
) -> typing.Callable[[typing.Callable[..., typing.Any]], "Pipeline"]:
    if any(c not in string.ascii_lowercase + string.digits + "_-" for c in code):
        raise Exception(
            "Pipeline name should contains only lower case letters, digits, '_' and '-'"
        )

    def decorator(fun):
        if isinstance(fun, FunctionWithParameter):
            parameters = fun.get_all_parameters()
        else:
            parameters = []

        return Pipeline(code, name, fun, parameters)

    return decorator


class PipelineRunError(Exception):
    pass


class Pipeline:
    def __init__(
        self,
        code: str,
        name: str,
        function: typing.Callable,
        parameters: typing.Sequence[Parameter],
    ):
        self.code = code
        self.name = name
        self.function = function
        self.parameters = parameters
        self.tasks = []

    def task(self, function):
        """task decorator"""

        return PipelineWithTask(function, self)

    def run(self, config: typing.Dict[str, typing.Any]):
        now = datetime.datetime.utcnow().replace(microsecond=0).isoformat()
        print(f'{now} Evaluating "{self.code}"')

        # Validate / default parameters
        validated_config = {}
        for parameter in self.parameters:
            value = config.pop(parameter.code, None)
            validated_value = parameter.validate(value)
            validated_config[parameter.code] = validated_value

        if len(config) > 0:
            raise ParameterValueError(
                f"The provided config contains invalid key(s): {', '.join(list(config.keys()))}"
            )

        self.function(**validated_config)

        # managing variables
        result_list = []
        context = get_context("spawn")
        pool = context.Pool()  # FIXME: set max size of pool

        while True:
            tasks = self.get_available_tasks()
            # filter already pooled task, even if they are not finished
            tasks = [t for t in tasks if not t.pooled]

            if len(tasks) == 0 and len(result_list) == 0:
                # nothing running, nothing to do
                break

            for task in tasks:
                now = datetime.datetime.utcnow().replace(microsecond=0).isoformat()
                print(f'{now} Started task "{task.compute.__name__}"')
                result = pool.apply_async(task.run)
                result_list.append((result, task))
                task.pooled = True

            while True:
                dag_step = False

                for result, task in result_list:
                    if not result.ready():
                        continue
                    now = (
                        datetime.datetime.now(tz=datetime.timezone.utc)
                        .replace(microsecond=0)
                        .isoformat()
                    )
                    print(f'{now} Finished task "{task.compute.__name__}"')
                    try:
                        task_com_result = result.get()
                        task.result = task_com_result.result
                        task.start_time = task_com_result.start_time
                        task.end_time = task_com_result.end_time
                        dag_step = True
                    except Exception as e:  # NOQA
                        raise PipelineRunError(f"Pipeline failed: {e}")

                if dag_step:
                    # remove finished tasks
                    result_list = [(r, t) for r, t in result_list if not r.ready()]
                    break
                else:
                    # busy loop
                    time.sleep(0.3)

        pool.close()
        pool.join()

    def get_available_tasks(self):
        return [task for task in self.tasks if task.is_ready()]

    def parameters_spec(self):
        return {arg.code: arg.parameter_spec() for arg in self.parameters}

    def __call__(self, config: typing.Optional[typing.Dict[str, typing.Any]] = None):
        if config is None:  # Called without arguments, in the pipeline file itself
            parser = argparse.ArgumentParser(exit_on_error=False)
            parser.add_argument("-c", "--config")
            parser.add_argument("-f", "--config-file")
            # We can't use parse_args, as it will call sys.exit() if there are unrecognized arguments
            args, argv = parser.parse_known_args()
            if argv or (args.config_file is not None and args.config is not None):
                raise ValueError(
                    f"Unrecognized arguments: {' '.join(argv)}. Running a pipeline requires a single "
                    "argument: either an inline JSON config with the --values/-v argument, or a JSON "
                    "config file with the --values-file/-f argument."
                )
            if args.config_file is not None:
                with open(args.config_file, "r") as cf:
                    try:
                        config = json.load(cf)
                    except json.JSONDecodeError:
                        raise ValueError("The provided config is not valid JSON")

            elif args.config is not None:
                try:
                    config = json.loads(args.config)
                except json.JSONDecodeError:
                    raise ValueError("The provided config is not valid JSON")
            else:
                config = {}

        self.run(config)
