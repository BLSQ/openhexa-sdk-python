from openhexa.sdk import current_run, pipeline


@pipeline("simple_pipeline", name="simple_pipeline")
def simple_pipeline():
    count = task_1()
    task_2(count)


@simple_pipeline.task
def task_1():
    current_run.log_info("In task 1...")

    return 42


@simple_pipeline.task
def task_2(count):
    current_run.log_info(f"In task 2... count is {count}")


if __name__ == "__main__":
    simple_pipeline()
