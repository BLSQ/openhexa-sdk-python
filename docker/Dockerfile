FROM blsq/openhexa-base-notebook:latest
WORKDIR /home/jovyan/

# FIXME: Replace this by a simple pip install openhexa.sdk when the package is published
ADD *.whl /home/jovyan/dist/
RUN pip install /home/jovyan/dist/*.whl


COPY bootstrap.py /home/jovyan/bootstrap.py
RUN find /home/jovyan/

ENTRYPOINT ["python", "/home/jovyan/bootstrap.py"]
CMD ["--help"]
