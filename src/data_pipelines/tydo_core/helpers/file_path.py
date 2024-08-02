import os

AIRFLOW_HOME = os.getenv('AIRFLOW_HOME', '/opt/airflow')
AIRFLOW_DATA_HOME = os.getenv('AIRFLOW_DATA_HOME', 'data_pipelines/tydo_core/data')


def _get_filepath(context, file):
  return os.path.join(AIRFLOW_HOME, 'dags', AIRFLOW_DATA_HOME, context, file)


def get_input_filepath(file):
  return _get_filepath('input', file)


def get_output_filepath(file):
  return _get_filepath('output', file)
