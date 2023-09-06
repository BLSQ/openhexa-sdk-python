from openhexa.sdk import current_run, pipeline, parameter


@pipeline("test-pipeline", name="test_pipeline", timeout=5000)
@parameter(
    "param1",
    name="First parameter",
    type=str,
)
@parameter(
    "param2",
    type=str,
    multiple=True,
    help="This is the second parameter",
)
@parameter("param3", name="Third parameter", type=int, default=2)
def test_pipeline(param1: str, param2: str, param3: int):
    count = task_1(param1=param3)
    task_2(param2)
    task_3(count)


@test_pipeline.task
def task_1(param):
    current_run.log_info("In task 1...")

    return param + 1


@test_pipeline.task
def task_2(param):
    current_run.log_info(f"In task 2... param :  {param}")


@test_pipeline.task
def task_3(param):
    current_run.log_info(f"In task 3... param :  {param}")


if __name__ == "__main__":
    test_pipeline()
