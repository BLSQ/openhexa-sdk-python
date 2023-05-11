FROM blsq/openhexa-base-notebook:latest
WORKDIR /home/jovyan/

RUN pip install openhexa.sdk==0.1.14

COPY bootstrap.py /home/jovyan/bootstrap.py
RUN find /home/jovyan/

ENTRYPOINT ["python", "/home/jovyan/bootstrap.py"]
CMD ["--help"]
