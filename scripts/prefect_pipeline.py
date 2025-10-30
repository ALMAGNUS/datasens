from prefect import flow, task


@task
def bronze_to_silver():
    return "ok"


@task
def silver_to_gold(_: str):
    return "ok"


@flow
def datasens_e1_flow():
    s = bronze_to_silver()
    g = silver_to_gold(s)
    return g


if __name__ == "__main__":
    result = datasens_e1_flow()
    print(result)


