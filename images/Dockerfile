FROM blsq/openhexa-base-environment:latest

USER root

WORKDIR /app
COPY . /app

RUN pip install build
RUN python -m build .

RUN pip install --no-cache-dir /app/dist/*.tar.gz && rm -rf /app/dist/*.tar.gz