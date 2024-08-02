import pandas as pd
from data_pipelines.tydo_core.helpers.logger import create_logger

logger = create_logger(context="DATA_READ_CSV")

# Data Ingestion
def retrieve_data(file_path: str) -> pd.DataFrame:
    """
    Reads data from a CSV file.
    :param file_path: Path to the CSV file.
    :return: pandas DataFrame.
    """
    # Read the data
    data = pd.read_csv(file_path, low_memory=False)

    logger.info("Read file", file=file_path)

    return data
