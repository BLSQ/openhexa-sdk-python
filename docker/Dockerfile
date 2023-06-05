FROM blsq/openhexa-base-notebook:0.13.0
WORKDIR /home/jovyan/

RUN pip install openhexa.sdk==0.1.17

COPY bootstrap.py /home/jovyan/bootstrap.py
RUN find /home/jovyan/

ENTRYPOINT ["python", "/home/jovyan/bootstrap.py"]
CMD ["--help"]
