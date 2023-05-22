from openhexa.sdk import current_run, pipeline


@pipeline("race_condition", name="Race condition")
def race_condition():
    r1 = one()
    r2 = two()
    r3 = three()

    four(r1, r2, r3)


@race_condition.task
def one():
    current_run.log_info("One...")

    return 1


@race_condition.task
def two():
    current_run.log_info("Two...")

    return 2


@race_condition.task
def three():
    current_run.log_info("Three...")

    return 3


@race_condition.task
def four(one, two, three):
    total = one + two + three
    current_run.log_info(f"Total is {total}")


if __name__ == "__main__":
    race_condition()
