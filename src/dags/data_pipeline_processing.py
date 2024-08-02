from airflow import DAG
from pendulum import datetime
from airflow.operators.python import PythonOperator
from data_pipelines.tydo_core.exporters.main import export_data
from data_pipelines.tydo_core.helpers.logger import create_logger


logger = create_logger(context="data_pipeline_processing")

def dg_1(ti):
    logger.info("dg_1 executed")
    ti.xcom_push(key="dg_p", value=1)


def dg_2(ti):
    value = ti.xcom_pull(key="dg_p")
    logger.info("dg_2 executed", value=value)
    ti.xcom_push(key="dg_p", value=2)


def dg_3(ti):
    value = ti.xcom_pull(key="dg_p")
    logger.info("dg_3 executed", value=value)


with DAG(
    dag_id="collect_and_export_csv_data",
    schedule_interval='30 6 * * *',
    start_date=datetime(2023, 1, 1),
    catchup=False,
    default_args={'timezone': 'America/Sao_Paulo'},
    tags=["products-catalog"]
) as dag:

    dg1 = PythonOperator(
        task_id="dg_1",
        python_callable=dg_1,
        provide_context=True,
        dag=dag
    )

    dg2 = PythonOperator(
        task_id="dg_2",
        python_callable=dg_2,
        provide_context=True,
        dag=dag
    )

    dg3 = PythonOperator(
        task_id="dg_3",
        python_callable=dg_3,
        provide_context=True,
        dag=dag
    )

dg1 >> dg2 >> dg3