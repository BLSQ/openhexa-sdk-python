"""Classes and functions related to pipeline tasks.

See https://github.com/BLSQ/openhexa/wiki/Writing-OpenHEXA-pipelines#pipelines-and-tasks for more information.
"""

from __future__ import annotations

import datetime
import typing

import openhexa.sdk.pipelines.pipeline


class TaskCom:
    """Lightweight data transfer object allowing tasks to communicate.

    TaskCom instances also allow us to build the pipeline dependency graph.
    """

    def __init__(self, task):
        self.result = task.result
        self.start_time = task.start_time
        self.end_time = task.end_time


class Task:
    """Tasks are pipeline data processing code units.

    See https://github.com/BLSQ/openhexa/wiki/Writing-OpenHEXA-pipelines#pipelines-and-tasks for more information.
    """

    def __init__(self, function: typing.Callable):
        self.name = function.__name__
        self.compute = function
        self.inputs = []
        self.result = None
        self.start_time = None
        self.end_time = None
        self.task_args = {}
        self.task_kwargs = {}
        self.active = False
        self.pooled = False

    def is_ready(self) -> bool:
        """Determine whether the task is ready to be run.

        This involves checking whether tasks higher up in the dependency graph have been executed.
        """
        if not self.active:
            return False

        for a in self.task_args:
            if issubclass(type(a), Task) and a.end_time is None:
                return False
        for k, a in self.task_kwargs.items():
            if issubclass(type(a), Task) and a.end_time is None:
                return False

        return True if self.end_time is None else False

    def get_ready_tasks(self) -> list[Task]:
        """Find and return all tasks that can be launched at this point in time."""
        tasks = []
        for a in self.task_args:
            if issubclass(type(a), Task):
                if a.is_ready():
                    tasks.append(a)
                else:
                    tasks += a.get_ready_tasks()
        for k, a in self.task_kwargs.items():
            if issubclass(type(a), Task):
                if a.is_ready():
                    tasks.append(a)
                else:
                    tasks += a.get_ready_tasks()

        return list(set(tasks))

    def run(self) -> TaskCom:
        """Run the task.

        Returns
        -------
        TaskCom
            A TaskCom instance which can in turn be passed to other tasks.
        """
        if self.end_time:
            # already executed, return previous result
            return self.result

        # forge task inputs
        r_task_args = []
        for a in self.task_args:
            if issubclass(type(a), Task):
                # previous task; execute + fw results
                r_task_args.append(a.result)
            else:
                # normal parameters, follow up
                r_task_args.append(a)

        r_task_kwargs = {}
        for k, a in self.task_kwargs.items():
            if issubclass(type(a), Task):
                r_task_kwargs[k] = a.result
            else:
                r_task_kwargs[k] = a

        # execute the task
        self.start_time = datetime.datetime.now(datetime.timezone.utc)
        self.result = self.compute(*r_task_args, **r_task_kwargs)
        self.end_time = datetime.datetime.now(datetime.timezone.utc)

        # done!
        return TaskCom(self)

    def __call__(self, *task_args, **task_kwargs):
        """Wrap the task with args and kwargs and return it."""
        self.active = True  # uncalled tasks will be skipped
        # check that all inputs are tasks
        self.task_args = task_args
        self.task_kwargs = task_kwargs

        return self

    def __repr__(self):
        """Representation of the task using its name."""
        return self.name


class PipelineWithTask:
    """Pipeline with attached tasks, usually through the @task decorator."""

    def __init__(
        self,
        function: typing.Callable,
        pipeline: openhexa.sdk.pipelines.Pipeline,
    ):
        self.function = function
        self.pipeline = pipeline

    def __call__(self, *task_args, **task_kwargs) -> Task:
        """Attach the new task to the decorated pipeline and return it."""
        task = Task(self.function)(*task_args, **task_kwargs)
        self.pipeline.tasks.append(task)
        return task
