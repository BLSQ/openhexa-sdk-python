FROM blsq/openhexa-base-notebook:latest
WORKDIR /home/jovyan/

RUN pip install --no-cache-dir -U openhexa.sdk

COPY bootstrap.py /home/jovyan/bootstrap.py
RUN find /home/jovyan/

ENTRYPOINT ["python", "/home/jovyan/bootstrap.py"]
CMD ["--help"]
