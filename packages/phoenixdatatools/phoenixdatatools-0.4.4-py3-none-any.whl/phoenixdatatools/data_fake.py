import logging
import random

from faker import Faker
from pyspark.sql import DataFrame, SparkSession  # noqa : F401
from pyspark.sql import types as T

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

fake = Faker()


def generate_unique_value(
    existing_values: str,
    method: str,
    faker_instance: Faker,
    max_attempts: int = 1000
) -> str:
    """
    Generates a unique value using a specified Faker method.

    Args:
        existing_values: A set of existing values to ensure uniqueness.
        method: The Faker method to be used for generating values.
        faker_instance: Instance of Faker with the specified locale.
        max_attempts: Maximum number of attempts to find a unique value.

    Returns:
        A unique value as a string,
        or None if a unique value could not be found.

    Raises:
        ValueError: An error occurred while generating a unique value: `error`
    """
    try:
        for _ in range(max_attempts):
            value = getattr(faker_instance, method)()
            if value not in existing_values:
                existing_values.add(value)
                return value

    except Exception as e:
        raise ValueError(
            f"An error occurred while generating a unique value: {e}"
        )


def generate_data_frame(
    column_specs: list,
    num_rows: int,
    locale: str
) -> DataFrame:
    """
    Generates a Spark DataFrame with fake data based on column specifications.

    Args:
        column_specs:
            List of dictionaries where each dictionary contains:
            - 'name': Column name
            - 'type': Data type (e.g., 'cpf', 'ssn', 'curp', 'dni',
                'nit', 'codice_fiscale', 'first_name', 'last_name',
                'date_of_birth', 'email', 'postcode', 'boolean', 'language')
        num_rows:
            Number of rows to generate.
        locale:
            Locale for Faker instance (e.g., 'pt_BR', 'en_US').

    Returns:
        DataFrame: Spark DataFrame with generated data.

    Raises:
        ValueError: If an unsupported type is provided in column_specs.

    Examples:
        >>> from pyspark.sql import SparkSession
        >>> spark = SparkSession.builder.getOrCreate()

        >>> column_specs = [
        ...     {'name': 'CPF', 'type': 'cpf'},
        ...     {'name': 'Name', 'type': 'first_name'},
        ...     {'name': 'Birthdate', 'type': 'date_of_birth'},
        ...     {'name': 'OptIn', 'type': 'boolean'}
        ... ]

        >>> num_rows = 5
        >>> df = generate_data_frame(column_specs, num_rows, 'pt_BR')

        ***Logs:***

        - INFO: Data generation started with locale 'pt_BR'.

        - INFO: DataFrame created successfully.

        - ERROR: Unsupported type 'unknown_type' in column 'unknown'.

        - ERROR:
            Error generating data for column 'CPF':
                ValueError('Unsupported type').

        - ERROR: Error creating DataFrame: Exception('Spark error').
    """
    fake = Faker(locale)
    spark = SparkSession.builder.getOrCreate()

    unique_fields = {
        'cpf': set(),
        'ssn': set(),
        'curp': set(),
        'dni': set(),
        'nit': set(),
        'codice_fiscale': set()
    }

    data = []
    logger.info(f"Data generation started with locale '{locale}'.")

    for _ in range(num_rows):
        row = []
        for col_spec in column_specs:
            col_name = col_spec['name']
            col_type = col_spec['type'].lower()

            try:
                if col_type in unique_fields:
                    value = generate_unique_value(
                        unique_fields[col_type], col_type, fake
                    )
                else:
                    if hasattr(fake, col_type):
                        value = getattr(fake, col_type)()
                        if col_type == 'date_of_birth':
                            value = value.strftime('%Y-%m-%d')

                    elif col_type == 'language':
                        value = random.choice(['PT', 'EN'])
                    elif col_type == 'boolean':
                        value = random.choice([True, False])
                    else:
                        logger.error(
                            f"Unsupported type '{col_type}' "
                            f"in column '{col_name}'."
                        )
                        raise ValueError(
                            f"Unsupported type '{col_type}' "
                            f"in column '{col_name}'."
                        )

                row.append(value)

            except Exception as e:
                logger.error(
                    f"Error generating data for column '{col_name}': {e}"
                )
                raise

        data.append(row)

    columns = [col_spec['name'] for col_spec in column_specs]
    schema = T.StructType(
        [T.StructField(name, T.StringType(), True) for name in columns]
    )

    try:
        dataframe = spark.createDataFrame(data, schema)
        logger.info("DataFrame created successfully.")
        return dataframe

    except Exception as e:
        logger.error(f"Error creating DataFrame: {e}")
        raise
