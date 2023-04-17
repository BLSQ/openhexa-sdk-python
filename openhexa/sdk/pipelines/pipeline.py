from __future__ import annotations

import argparse
import datetime
import json
import string
import time
import typing
from logging import getLogger

from multiprocess import get_context

from .arguments import Argument, ArgumentValueError, FunctionWithArgument
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
        if isinstance(fun, FunctionWithArgument):
            arguments = fun.get_all_arguments()
        else:
            arguments = []

        return Pipeline(code, name, fun, arguments)

    return decorator


class PipelineRunError(Exception):
    pass


class Pipeline:
    def __init__(
        self,
        code: str,
        name: str,
        function: typing.Callable,
        arguments: typing.Sequence[Argument],
    ):
        self.code = code
        self.name = name
        self.function = function
        self.arguments = arguments
        self.tasks = []

    def task(self, function):
        """task decorator"""

        return PipelineWithTask(function, self)

    def run(self, config: typing.Dict[str, typing.Any]):
        now = datetime.datetime.utcnow().replace(microsecond=0).isoformat()
        print(f'{now} Evaluating "{self.code}"')

        # Validate / default arguments
        validated_config = {}
        for single_argument in self.arguments:
            value = config.pop(single_argument.code, None)
            validated_value = single_argument.validate(value)
            validated_config[single_argument.code] = validated_value

        if len(config) > 0:
            raise ArgumentValueError(
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
        return {arg.code: arg.parameter_spec() for arg in self.arguments}

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
