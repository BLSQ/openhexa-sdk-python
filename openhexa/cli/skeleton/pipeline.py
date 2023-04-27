from openhexa.sdk import current_run, pipeline


@pipeline("skeleton-pipeline-code", name="Skeleton pipeline name")
def skeleton_pipeline_name():
    count = task_1()
    task_2(count)


@skeleton_pipeline_name.task
def task_1():
    current_run.log_info("In task 1...")

    return 42


@skeleton_pipeline_name.task
def task_2(count):
    current_run.log_info(f"In task 2... count is {count}")


if __name__ == "__main__":
    skeleton_pipeline_name()
