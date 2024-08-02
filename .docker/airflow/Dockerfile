FROM apache/airflow:2.6.3-python3.10

USER airflow

WORKDIR $AIRFLOW_HOME

RUN pip install --user --upgrade pip

COPY requirements.txt requirements.txt

COPY .docker/airflow/airflow.cfg airflow.cfg

RUN pip install --no-cache-dir --user -r requirements.txt
