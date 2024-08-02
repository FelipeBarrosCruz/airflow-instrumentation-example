from data_pipelines.tydo_core.transformations.main import integrate_treated_data
from data_pipelines.tydo_core.helpers.file_path import get_output_filepath
import requests
import os
from data_pipelines.tydo_core.helpers.logger import create_logger


AIRFLOW_HOME = os.getenv('AIRFLOW_HOME', '/opt/airflow')

HEALTH_CHECK_URL = os.getenv('HEALTH_CHECK_URL')

logger = create_logger(context="DATA_EXPORT_STATS_MEASURES")

def export_data(file_name='processed_data.json'):
    processed_data = integrate_treated_data()
    logger.info("ACCESSING PROCESSED DATA")

    json_path = get_output_filepath(file_name)
    logger.info("Prepare to export", file=json_path)

    processed_data.to_json(json_path, orient='records', lines=True)
    logger.info("Data exported", file=json_path)

    if not os.path.exists(json_path):
        raise Exception("File not exported succefully")
    
    if HEALTH_CHECK_URL:
        response = requests.get(HEALTH_CHECK_URL)
        logger.info("Health Check", status=response.status_code)