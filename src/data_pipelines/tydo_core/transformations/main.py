from data_pipelines.tydo_core.helpers.logger import create_logger
from data_pipelines.tydo_core.collectors.main import retrieve_data
from data_pipelines.tydo_core.helpers.file_path import get_input_filepath
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
import pandas as pd
import os

AIRFLOW_HOME = os.getenv('AIRFLOW_HOME')


logger = create_logger(context="TRANSFORM_DATA")

# Statistical Measures Function
def calculate_statistical_measures(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("calculate_statistical_measures")
    """
    Calculates mean, median, and standard deviation for all numerical columns in a DataFrame.
    :param df: pandas DataFrame.
    :return: DataFrame with statistical measures for each numerical column.
    """
    numerical_cols = df.select_dtypes(include=['number']).columns
    stats = pd.DataFrame({
        'Mean': df[numerical_cols].mean(),
        'Median': df[numerical_cols].median(),
        'Standard Deviation': df[numerical_cols].std()
    })
    return stats


# Normalization
def normalize_column(df: pd.DataFrame, column_name: list[str]):
    """
    Normalizes a numerical column in the DataFrame to a range of 0 to 1.
    :param df: pandas DataFrame.
    :param column_name: Name of the column to be normalized.
    :return: DataFrame with the normalized column.
    """
    scaler = MinMaxScaler()
    df[column_name] = scaler.fit_transform(df[[column_name]])
    return df

# Categorization (One-Hot Encoding)
def categorize_column(df, column_name):
    """
    Applies one-hot encoding to a categorical column in the DataFrame.
    :param df: pandas DataFrame.
    :param column_name: Name of the column to be categorized.
    :return: DataFrame with one-hot encoded columns.
    """
    onehot = OneHotEncoder()
    encoded = onehot.fit_transform(df[[column_name]]).toarray()
    categories = onehot.categories_[0]
    for i, category in enumerate(categories):
        df[f"{column_name}_{category}"] = encoded[:, i]
    return df.drop(column_name, axis=1)

def fill_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    # Handle missing values by filling with the mean
    return df.fillna(df.mean(numeric_only=True))

def integrate_treated_data() -> pd.DataFrame:
    logger.info("starting to integrate csv data with: integrate_treated_data")
    csv_path = get_input_filepath("sample_data_file.csv")
    
    # Data ingestion and cleaning
    data = fill_missing_values(retrieve_data(csv_path))

    # Calculate statistical measures
    stats = calculate_statistical_measures(data)
    logger.info("Statistical Measures", head=stats.head())

    # Apply normalization
    normalized_data = normalize_column(data.copy(), 'AGE')
    data['AGE_normalized'] = normalized_data['AGE']

    logger.info("Normalized Data", head=normalized_data[['AGE']].head())
    
    # Apply categorization (one-hot encoding)
    categorized_data = categorize_column(data.copy(), 'GENDER')
    logger.info("Categorized Data", head=categorized_data[['GENDER_F', 'GENDER_M', 'GENDER_nan']].head())
    
    for col in categorized_data.columns:
        if col.startswith('GENDER_'):
            data[col] = categorized_data[col]

    return data