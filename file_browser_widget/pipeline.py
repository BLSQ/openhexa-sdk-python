"""Template for newly generated pipelines."""

from openhexa.sdk import File, current_run, pipeline


@pipeline("file_browser_widget")
@parameter("catt_file", name="Select a file", type=File, required=True, default="catt.xml")
def file_browser_widget(catt_file):
    """Write your pipeline orchestration here.

    Pipeline functions should only call tasks and should never perform IO operations or expensive computations.
    """
    print(catt_file)
    current_run.log_info(catt_file)
    count = task_1()
    task_2(count)


@file_browser_widget.task
def task_1():
    """Put some data processing code here."""
    current_run.log_info("In task 1...")

    return 42


@file_browser_widget.task
def task_2(count):
    """Put some data processing code here."""
    current_run.log_info(f"In task 2... count is {count}")


if __name__ == "__main__":
    file_browser_widget()
