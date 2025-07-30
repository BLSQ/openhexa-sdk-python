FROM blsq/openhexa-base-environment:latest

USER root

WORKDIR /home/hexa
COPY . /home/hexa

RUN pip install build
RUN python -m build .

RUN pip install --no-cache-dir /home/hexa/dist/*.tar.gz && rm -rf /home/hexa/dist/*.tar.gz