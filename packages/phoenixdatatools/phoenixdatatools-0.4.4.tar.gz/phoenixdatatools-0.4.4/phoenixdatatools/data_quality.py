import logging
from datetime import datetime

from pyspark.sql import DataFrame  # noqa: F401
from pyspark.sql.functions import (  # noqa: F401
    col,
    count,
    current_timestamp,
    sum,
    to_date,
    to_timestamp,
    when,
)
from pyspark.sql.types import (  # noqa: F401
    BooleanType,
    DateType,
    FloatType,
    IntegerType,
    LongType,
    StringType,
    TimestampType,
)


def not_null_test(
    data_frame: DataFrame,
    required_columns: dict
) -> bool:
    """
    Performs the test for non-null and non-blank values
    in one or more columns of a DataFrame.

    Args:
        data_frame: Input DataFrame to perform Data Quality checks on.
        required_columns: Dictionary where keys are column names and values
            are "error" or "warning" indicating the action to take
            if the column has null or blank values.

    Returns:
        boolean: True if all checks pass, False otherwise.

    Raises:
        Exception: If any of the checks fail.

    Examples:
        >>> from pyspark.sql import SparkSession

        >>> from pyspark.sql.types import StructType, StructField, StringType

        >>> spark = SparkSession.builder.getOrCreate()

        >>> data = [
        ...     ("123.456.789-00", "Maria Silva", ""),
        ...     ("987.654.321-00", "Joao Souza", "joao.souza@example.com"),
        ...     (None, "Carlos Pereira", "carlos.pereira@example.com")
        ... ]

        >>> schema = StructType([
        ...     StructField("cpf", StringType(), True),
        ...     StructField("full_name", StringType(), True),
        ...     StructField("email", StringType(), True)
        ... ])

        >>> df = spark.createDataFrame(data, schema)

        >>> required_columns = {
        ...     "cpf": "error",
        ...     "email": "warning"
        ... }

        >>> try:
        ...     result = not_null_test(df, required_columns)
        ... except Exception as e:
        ...     print(e)
        Not Null Test Failed: Columns with NULL or blank values found!

        ***Logs:***

        - ERROR: Not Null Test Failed: cpf has 1 NULL or blank values!

        - WARNING: Not Null Test Warning: email has 1 NULL or blank values!

        - Exception: Not Null Test Failed: Columns with NULL or blank values found!  # noqa : E501
    """

    for column in required_columns.keys():
        if column not in data_frame.columns:
            print(
                f"Not Null Test Failed: {column} "
                "is not present in the DataFrame!"
            )
            raise Exception(
                f"Not Null Test Failed: {column} "
                "is not present in the DataFrame!"
            )

    data_frame.cache()

    null_counts = data_frame.select(
        [
            sum(
                col(c).isNull().cast('int')
            ).alias(c) for c in required_columns.keys()
        ]
    ).collect()[0].asDict()

    all_checks_pass = True
    failed_columns = []

    for column, action in required_columns.items():
        null_count = null_counts[column]

        if null_count > 0:
            failed_columns.append((column, null_count, action))
            if action == "error":
                all_checks_pass = False
                print(
                    f"Not Null Test Failed: {column} "
                    f"has {null_count} NULL or blank values!"
                )
                logging.error(
                    f"Not Null Test Failed: {column} "
                    f"has {null_count} NULL or blank values!"
                )
            elif action == "warning":
                all_checks_pass = False
                print(
                    f"Not Null Test Warning: {column} "
                    f"has {null_count} NULL or blank values!"
                )
                logging.warning(
                    f"Not Null Test Warning: {column} "
                    f"has {null_count} NULL or blank values!"
                )

    if all_checks_pass:
        print(
            "Data Quality Check: Successfully processed Null record test."
        )
        logging.info(
            "Data Quality Check: Successfully processed Null record test."
        )

    data_frame.unpersist()

    if any(action == "error" for _, _, action in failed_columns):
        print(
            "Not Null Test Failed: Columns with NULL or blank values found!"
        )
        raise Exception(
            "Not Null Test Failed: Columns with NULL or blank values found!"
        )

    return all_checks_pass


def uniqueness_test(data_frame: DataFrame, primary_key_columns: list) -> bool:
    """
    Performs the test for unique values
    in one or more columns of a DataFrame.

    Args:
        data_frame: Input DataFrame to perform Data Quality checks on.
        primary_key_columns: List of primary key column names.

    Returns:
        bool: True if checks pass, False otherwise.

    Raises:
        Exception: If Data Quality checks fail.

    Examples:
        >>> from pyspark.sql import SparkSession

        >>> from pyspark.sql.types import StructType, StructField, StringType

        >>> spark = SparkSession.builder.getOrCreate()

        >>> data = [
        ...     ("123.456.789-00", "Maria Silva", "maria@example.com"),
        ...     ("123.456.789-00", "Joao Souza", "joao.souza@example.com"),
        ...     (None, "Carlos Pereira", "carlos.pereira@example.com")
        ... ]

        >>> schema = StructType([
        ...     StructField("cpf", StringType(), True),
        ...     StructField("full_name", StringType(), True),
        ...     StructField("email", StringType(), True)
        ... ])

        >>> df = spark.createDataFrame(data, schema)

        >>> primary_key_columns = ["cpf"]

        >>> try:
        ...     result = uniqueness_test(df, primary_key_columns)
        ... except Exception as e:
        ...     print(e)
        Data Quality Check Failed: Found 1 duplicate records!

        ***Logs:***

        - ERROR: Data Quality Check Failed: Found 1 duplicate records!

        - INFO: Data Quality Check: Successfully processed duplicate record test.  # noqa : E501
    """
    # Check for duplicate records based on primary key
    duplicate_count = data_frame.groupBy(
        primary_key_columns).count().filter("count > 1").count()

    if duplicate_count > 0:
        print(
            f"Data Quality Check Failed: Found {duplicate_count}"
            " duplicate records!"
        )
        raise Exception(
            f"Data Quality Check Failed: Found {duplicate_count}"
            " duplicate records!"
        )
    else:
        print(
            "Data Quality Check: Successfully processed duplicate record test."
        )
        logging.info(
            "Data Quality Check: Successfully processed duplicate record test."
        )
        return True


def relationship_test(
    foreign_dataframe: DataFrame,
    target_dataframe: DataFrame,
    df_foreign_key: str,
    target_dataframe_key: str
) -> bool:
    """
    Performs the relationship test (referential integrity)
    between two DataFrames based on a foreign key of the first DataFrame
    and the primary key of the target DataFrame.

    Args:
        foreign_dataframe:
            Input DataFrame that foreign key will be checked
            for referential integrity.
        target_dataframe:
            Input DataFrame against which your primary key will be checked
            for referential integrity.
        df_foreign_key:
            Foreign key of the first DataFrame.
        target_dataframe_key:
            Primary key of the second DataFrame.

    Returns:
        bool: True if checks pass, False otherwise.

    Raises:
        Exception: If Data Quality checks fail.

    Examples:
        >>> from pyspark.sql import SparkSession

        >>> from pyspark.sql.types import ( # noqa : F401
        ...     StructType,
        ...     StructField,
        ...     IntegerType,
        ...     StringType,
        ... )

        >>> spark = SparkSession.builder.getOrCreate()

        >>> foreign_data = [
        ...     (1, "Record1"),
        ...     (2, "Record2"),
        ...     (3, "Record3"),
        ...     (4, "Record4")
        ... ]

        >>> foreign_columns = ["id", "value"]

        >>> target_data = [
        ...     (1, "Target1"),
        ...     (2, "Target2"),
        ...     (3, "Target3")
        ... ]

        >>> target_columns = ["id_target", "target_value"]

        >>> foreign_df = spark.createDataFrame(foreign_data, foreign_columns)
        >>> target_df = spark.createDataFrame(target_data, target_columns)

        >>> try:
        ...     result = relationship_test(
        ...         foreign_df,
        ...         target_df,
        ...         'id',
        ...         'id_target'
        ...     )
        ... except Exception as e:
        ...     print(e)
        Data Quality Check Failed: Found 1 unmatched records!

        ***Logs:***

        - ERROR: Data Quality Check Failed: Found 1 unmatched records!

        - INFO: Data Quality Check: Successfully processed relationship test.
    """

    joined_dataframe = foreign_dataframe.join(
        target_dataframe,
        foreign_dataframe[df_foreign_key] == target_dataframe[target_dataframe_key],  # noqa: E501
        "left"
    )

    unmatched_records_df = joined_dataframe.filter(
        col(target_dataframe_key).isNull()
    ).select(foreign_dataframe[df_foreign_key])

    if unmatched_records_df.count() > 0:
        print(
            f"Data Quality Check Failed: Found {unmatched_records_df.count()}"
            " unmatched records!"
        )
        raise Exception(
            f"Data Quality Check Failed: Found {unmatched_records_df.count()}"
            " unmatched records!"
        )
    print(
        "Data Quality Check: Successfully processed relationship test."
    )
    logging.info(
        "Data Quality Check: Successfully processed relationship test."
    )

    return True


def freshness_test(
    dataframe: DataFrame,
    updated_at_column: str,
    warn_after: int,
    error_after: int
) -> bool:
    """
    Performs the freshness (timeliness) test on a DataFrame.
    Ensures that the data in your DataFrame is recent
    or within the expected date.

    Args:
        dataframe:
            Input DataFrame.
        updated_at_column:
            Name of the updated at column in the DataFrame.
        warn_after:
            Threshold in days after which to warn about data staleness.
        error_after:
            Threshold in days after which to error about data staleness.

    Returns:
        bool: True if checks pass, False otherwise.

    Raises:
        Exception: If Data Quality checks fail.

    Examples:
        >>> from pyspark.sql import SparkSession

        >>> from pyspark.sql.functions import to_timestamp

        >>> from pyspark.sql.types import StructType, StructField, StringType

        >>> spark = SparkSession.builder.getOrCreate()

        >>> schema = StructType([
        ...     StructField("id", StringType(), True),
        ...     StructField("timestamp", StringType(), True)
        ... ])

        >>> data = [
        ...     ('A', '2024-07-26 19:31:39'),
        ...     ('B', '2024-07-26 19:31:39'),
        ...     ('C', '2024-07-26 19:31:39')
        ... ]

        >>> df = spark.createDataFrame(data, schema)

        >>> df = df.withColumn(
        ...     "timestamp",
        ...     to_timestamp("timestamp", "yyyy-MM-dd HH:mm:ss")
        ... )

        >>> try:
        ...     freshness_test(df, "timestamp", 2, 5)
        ... except Exception as e:
        ...     print(f"Exception: {e}")
        Exception: Data Quality Check Failed: Data is older than 5 days!

        ***Logs:***

        - ERROR: If data is older than `error_after` days.

        - WARNING: If data is older than `warn_after` days.

        - INFO: Data Quality Check: Successfully processed freshness test.
    """

    max_date = dataframe.agg({updated_at_column: "max"}).collect()[0][0]
    today = dataframe.select(
        current_timestamp().alias("today")
    ).collect()[0]["today"]

    if isinstance(max_date, str):
        max_date = datetime.strptime(max_date, '%Y-%m-%d %H:%M:%S')

    days_since_max = (today - max_date).days

    if days_since_max > error_after:
        print(
            "Data Quality Check Failed: "
            f"Data is older than {error_after} days!"
        )
        raise Exception(
            "Data Quality Check Failed: "
            f"Data is older than {error_after} days!"
        )
    elif days_since_max > warn_after:
        message_warning = (
            f"WARNING: Data is older than {warn_after} days."
        )
        logging.warning(message_warning)
        print(message_warning)
        return True
    else:
        print(
            "Data Quality Check: Successfully freshness test."
        )
        logging.info(
            "Data Quality Check: Successfully freshness test."
        )
        return True


def accepted_values_test(
    dataframe: DataFrame,
    column_name: str,
    valid_values: list
) -> bool:
    """
    Validates if a column in a DataFrame contains only accepted values.

    Args:
        dataframe:
            Input DataFrame.
        column_name:
            Name of the column to validate.
        valid_values:
            List of valid values for the column.

    Returns:
        bool: True if all values in the column are valid, false otherwise.

    Raises:
        ValueError: If the specified column does not exist in the DataFrame.

    Examples:
        >>> from pyspark.sql import SparkSession

        >>> from pyspark.sql.types import StructType, StructField, StringType

        >>> spark = SparkSession.builder.getOrCreate()

        >>> schema = StructType([
        ...     StructField("id", StringType(), True),
        ...     StructField("value", StringType(), True)
        ... ])

        >>> data = [("A", "PT"), ("B", "EN"), ("C", "PT")]

        >>> df = spark.createDataFrame(data, schema)

        >>> valid_values = ["FR", "EN"]

        >>> try:
        ...     result = accepted_values_test(df, "value", valid_values)
        ... except ValueError as e:
        ...     print(e)
        Invalid values found in column 'value': ['PT']

        ***Logs:***

        - INFO: Invalid values found in column 'value': ['value']

        - INFO: Data Quality Check: Successfully processed freshness test.
    """

    if column_name not in dataframe.columns:
        raise ValueError(
            f"Column '{column_name}' "
            "does not exist in the DataFrame."
        )

    invalid_values = dataframe.where(
        ~col(column_name).isin(valid_values)
    ).select(col(column_name)).distinct().collect()

    if invalid_values:
        invalid_values_list = [row[column_name] for row in invalid_values]
        message = f"Invalid values found in column '{column_name}': {invalid_values_list}" # noqa : E501
        logging.info(message)
        print(message)
        all_checks_pass = False
    else:
        message = "Data Quality Check: Successfully accepted values test."
        logging.info(message)
        print(message)
        all_checks_pass = True

    return all_checks_pass


def columns_type_test(
    dataframe: DataFrame,
    column_specs: dict
) -> bool:
    """
    Validates that the columns in a DataFrame match specified data types.

    This function checks if the columns
    in the provided DataFrame conform to the expected types.

    It can handle basic data types (e.g., string, int, float)
    as well as date and timestamp formats.

    Args:
        dataframe:
            The input DataFrame containing the data to be validated.

        column_specs:
            A dictionary where each key is a column name and each value is
            the expected data type. The expected type can be a string (e.g.,
            "string", "int", "float") or a tuple for date and timestamp types
            (e.g.,("date", "yyyy-MM-dd"), ("timestamp", "yyyy-MM-dd HH:mm:ss"))

    Returns:
        bool:
            Returns True if all columns are of the expected type.

            Returns False if any column fails the type validation,
            logging the details of the failure.

    Raises:
        ValueError:
            If an unsupported type is provided or if the column
            specified in the column_specs does not exist in the DataFrame.

    Examples:
        >>> from pyspark.sql import SparkSession

        >>> from pyspark.sql.types import StringType, StructType, StructField

        >>> spark = SparkSession.builder.getOrCreate()

        >>> schema = StructType([
        ...     StructField("id", StringType(), True),
        ...     StructField("date_column", StringType(), True),
        ...     StructField("name", StringType(), True)
        ... ])

        >>> data = [
        ...     ("123", "2023-07-15", "Alice"),
        ...     ("456", "2023-07-16", "Bob"),
        ...     ("789", "Invalid Date", "Charlie")
        ... ]

        >>> df = spark.createDataFrame(data, schema)

        >>> column_specs = {
        ...     "id": "string",
        ...     "date_column": ("date", "yyyy-MM-dd"),
        ...     "name": "string"
        ... }

        >>> result = columns_type_test(df, column_specs)
        >>> result
        False

        ***Logs:***

        - ERROR: Column 'date_column' failed date validation with format 'yyyy-MM-dd'.  # noqa : E501

        - INFO: Data Quality Check: Successfully validated column types.
    """

    type_mapping = {
        "string": StringType(),
        "int": IntegerType(),
        "float": FloatType(),
        "date": DateType(),
        "timestamp": TimestampType(),
        "boolean": BooleanType(),
        "long": LongType()
    }

    errors = []

    for column, expected_type in column_specs.items():
        if column not in dataframe.columns:
            errors.append(
                f"Column '{column}' does not exist in the DataFrame."
            )
            continue

        if isinstance(
            expected_type, tuple
        ) and expected_type[0] in ["date", "timestamp"]:

            date_format = expected_type[1]

            if expected_type[0] == "date":
                invalid_dates = dataframe.filter(
                    to_date(
                        col(column), date_format
                    ).isNull() & col(column).isNotNull()
                )
                invalid_count = invalid_dates.count()
            elif expected_type[0] == "timestamp":
                invalid_timestamps = dataframe.filter(
                    to_timestamp(
                        col(column), date_format
                    ).isNull() & col(column).isNotNull()
                )
                invalid_count = invalid_timestamps.count()

            if invalid_count > 0:
                errors.append(
                    f"Column '{column}' failed {expected_type[0]} "
                    f"validation with format '{date_format}'."
                )

        else:
            if expected_type not in type_mapping:
                message_not_type = (
                    f"Unsupported type '{expected_type}' for column '{column}'"
                )
                errors.append(message_not_type)
                print(message_not_type)
                logging.warning(message_not_type)
                continue

            actual_type = dataframe.schema[column].dataType

            if not isinstance(
                actual_type, type(type_mapping[expected_type])
            ):
                message_not_is = (
                    f"Column '{column}' has type '{actual_type}' "
                    f"but expected '{type_mapping[expected_type]}'."
                )
                errors.append(message_not_is)
                print(message_not_is)
                logging.warning(message_not_is)

                continue

    if errors:
        for error in errors:
            print(error)
            logging.error(error)
        return False

    print(
        "Data Quality Check: Successfully validated column types."
    )
    logging.info(
        "Data Quality Check: Successfully validated column types."
    )

    return True


def regex_pattern_test(
    dataframe: DataFrame,
    column_name: str,
    pattern: str
) -> bool:
    """
    Validates that the values in a column match
    a specified regular expression pattern.

    Args:
        dataframe:
            Input DataFrame.
        column_name:
            Name of the column to validate.
        pattern:
            Regular expression pattern to match.

    Returns:
        bool: True if all values match the pattern, False otherwise.

    Raises:
        ValueError: If the column does not exist in the DataFrame.

    Examples:
        >>> from pyspark.sql import SparkSession
        >>> from pyspark.sql.types import StructType, StructField, StringType

        >>> spark = SparkSession.builder.getOrCreate()

        >>> schema = StructType([
        ...     StructField("id", StringType(), True),
        ...     StructField("email", StringType(), True)
        ... ])

        >>> data = [
        ...     ("1", "test@example.com"),
        ...     ("2", "invalid-email"),
        ...     ("3", "user@domain.com")
        ... ]

        >>> df = spark.createDataFrame(data, schema)

        >>> pattern = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        >>> try:
        ...     regex_pattern_test(df, "email", pattern)
        ... except ValueError as e:
        ...     print(e)
        Invalid values found in 'email': ['invalid-email']
        False

        ***Logs:***

        - INFO: Invalid values found in column 'email': ['invalid-email']

        - INFO: Data Quality Check: Successfully processed regex pattern test.

        ***Pattern examples:***

        - CPF: "^(?:\d{3}\.\d{3}\.\d{3}-\d{2}|\d{11})$" # noqa : W605

        - CNPJ: "^(?:\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}|\d{14})$"

        - E-mail: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        - Birth date dd/mm/yyyy: "^(?:0[1-9]|[12][0-9]|3[01])/(?:0[1-9]|1[0-2])/\d{4}$"

        - Date format yyyy-mm-dd: "^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$"

        - Brazil phone: "^\(?\d{2}\)?\s?\d{4,5}-\d{4}$"
    """
    if column_name not in dataframe.columns:
        raise ValueError(
            f"Column '{column_name}' does not exist in the DataFrame."
        )

    invalid_values = dataframe.filter(
        ~col(column_name).rlike(pattern)
    ).select(column_name).distinct().collect()

    if invalid_values:
        invalid_values_list = [row[column_name] for row in invalid_values]
        logging.info(
            f"Invalid values found in '{column_name}': {invalid_values_list}"
        )
        print(
            f"Invalid values found in '{column_name}': {invalid_values_list}"
        )
        return False

    logging.info(
        "Data Quality Check: Successfully processed regex pattern test."
    )
    print(
        "Data Quality Check: Successfully processed regex pattern test."
    )
    return True


def range_test(
    dataframe: DataFrame,
    column_name: str,
    min_value: float,
    max_value: float
) -> bool:
    """
    Validates that the values in a numeric column
    fall within a specified range.

    Args:
        dataframe: Input DataFrame.
        column_name: Name of the column to validate.
        min_value: Minimum acceptable value.
        max_value: Maximum acceptable value.

    Returns:
        bool: True if all values are within the range, False otherwise.

    Raises:
        ValueError:
            If the column does not exist in the DataFrame or is not numeric.

    Examples:
        >>> from pyspark.sql import SparkSession
        >>> from pyspark.sql.types import StructType, StructField, IntegerType

        >>> spark = SparkSession.builder.getOrCreate()

        >>> schema = StructType([
        ...     StructField("id", IntegerType(), True),
        ...     StructField("score", IntegerType(), True)
        ... ])

        >>> data = [(1, 10), (2, 15), (3, 25), (4, 5)]

        >>> df = spark.createDataFrame(data, schema)

        >>> try:
        ...     range_test(df, "score", 0, 20)
        ... except ValueError as e:
        ...     print(e)
        False

        ***Logs:***

        - INFO: Invalid values found in column `columns`: `value`

        - INFO: Data Quality Check: Successfully processed range test.
    """
    if column_name not in dataframe.columns:
        print(
            f"Column '{column_name}' does not exist in the DataFrame."
        )
        raise ValueError(
            f"Column '{column_name}' does not exist in the DataFrame."
        )

    invalid_values = dataframe.filter(
        (col(column_name) < min_value) | (col(column_name) > max_value)
    ).select(column_name).distinct().collect()

    if invalid_values:
        invalid_values_list = [row[column_name] for row in invalid_values]
        print(
            f"Invalid values found in column '{column_name}'"
            f": {invalid_values_list}"
        )
        logging.info(
            f"Invalid values found in column '{column_name}'"
            f": {invalid_values_list}"
        )
        return False

    print(
        "Data Quality Check: Successfully processed range test."
    )
    logging.info(
        "Data Quality Check: Successfully processed range test."
    )

    return True
