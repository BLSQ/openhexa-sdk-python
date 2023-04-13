from __future__ import annotations

import datetime
import typing

import openhexa.sdk.pipelines.pipeline


class TaskCom:
    def __init__(self, task):
        self.result = task.result
        self.start_time = task.start_time
        self.end_time = task.end_time


class Task:
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

    def __call__(self, *task_args, **task_kwargs):
        self.active = True  # uncalled tasks will be skipped
        # check that all inputs are tasks
        self.task_args = task_args
        self.task_kwargs = task_kwargs
        return self

    def __repr__(self):
        return self.name

    def get_node_inputs(self):
        inputs = []
        for a in self.task_args:
            if issubclass(type(a), Task):
                inputs.append(a)
        for k, a in self.task_kwargs.items():
            if issubclass(type(a), Task):
                inputs.append(a)
        return inputs

    def is_ready(self):
        if not self.active:
            return False

        for a in self.task_args:
            if issubclass(type(a), Task) and a.end_time is None:
                return False
        for k, a in self.task_kwargs.items():
            if issubclass(type(a), Task) and a.end_time is None:
                return False

        return True if self.end_time is None else False

    def get_tasks_ready(self):
        tasks = []
        for a in self.task_args:
            if issubclass(type(a), Task):
                if a.is_ready():
                    tasks.append(a)
                else:
                    tasks += a.get_tasks_ready()
        for k, a in self.task_kwargs.items():
            if issubclass(type(a), Task):
                if a.is_ready():
                    tasks.append(a)
                else:
                    tasks += a.get_tasks_ready()

        return list(set(tasks))

    def run(self):
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

    def stateless_run(self):
        self.result = None
        self.start_time, self.end_time = None, None
        return self.run()


class PipelineWithTask:
    def __init__(
        self,
        function: typing.Callable,
        pipeline: openhexa.sdk.pipelines.pipeline.Pipeline,
    ):
        self.function = function
        self.pipeline = pipeline

    def __call__(self, *task_args, **task_kwargs):
        task = Task(self.function)(*task_args, **task_kwargs)
        self.pipeline.tasks.append(task)
        return task
