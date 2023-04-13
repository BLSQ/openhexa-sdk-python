# OpenHexa Python SDK

## Running the examples

Clone the repo and install the dependencies, including the ones required to run the examples:

```shell
git checkout https://github.com/BLSQ/openhexa-sdk-python.git
pip install ".[examples]"
```

Run a pipeline:

```shell
cd examples/pipelines/logistic_stats
python pipeline.py -c '{"deg":"qfxEYY9xAl6","periods":["2022Q1","2022Q2"]}'
```

Or using a config file:

```shell
cd examples/pipelines/logistic_stats
python pipeline.py -f example_conf.json
```

## Development & testing

Install the SDK in editable mode:

```shell
pip install -e ".[dev]"
```

Run the tests using pytest:

```shell
pytest
```