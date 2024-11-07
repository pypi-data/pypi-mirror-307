import logging

import matplotlib.pyplot as plt
import pyspark.sql.functions as F
import seaborn as sns
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, countDistinct
from pyspark.sql.functions import max as spark_max
from pyspark.sql.functions import min as spark_min
from pyspark.sql.types import (
    DecimalType,
    DoubleType,
    FloatType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)


def standard_analyses(
    df: DataFrame,
    numeric_columns: list = None
) -> DataFrame:
    """
    Perform statistical analysis on columns of the DataFrame.

    Args:
        df: The input DataFrame for analysis.
        numeric_columns:
            List of column names that are considered numeric.
            If not provided, all columns are treated as categorical.
            - For numeric columns, the function calculates
                the minimum and maximum values.
            - For non-numeric columns, it calculates
                the count of distinct values.

    Returns:
        DataFrame: DataFrame with the statistics columns:
            - Column: Name of the column.
            - DistinctCount: Count of distinct values (for non-numeric columns)
            - NullCount: Number of null values in the column.
            - NullPercentage: Percentage of null values in the column.
            - MinValue: Minimum value (for numeric columns).
            - MaxValue: Maximum value (for numeric columns).

    Raises:
        ValueError:
            If any specified numeric column does not exist in the DataFrame.

    Examples:
        >>> from pyspark.sql import SparkSession
        >>> from pyspark.sql.types import StructType, StructField, IntegerType, StringType  # noqa : E501

        >>> spark = SparkSession.builder.getOrCreate()

        >>> schema = StructType([
        ...     StructField("id", IntegerType(), True),
        ...     StructField("score", IntegerType(), True),
        ...     StructField("category", StringType(), True)
        ... ])

        >>> data = [(1, 10, "A"), (2, 15, "B"), (3, 25, "A"), (4, 5, "C")]

        >>> df = spark.createDataFrame(data, schema)

        >>> try:
        ...     analysis_df = standard_analyses(df, numeric_columns=["score"])
        ... except ValueError as e:
        ...     print(e)

        ***Logs:***

        - INFO: Total rows in the DataFrame: `rows_number`
        - INFO: Processing column `id`
        - INFO: Processing column `score`
        - INFO: Processing column `category`
        - INFO: Data Quality Check: Successfully processed standard analysis.
    """

    if numeric_columns is None:
        numeric_columns = []

    total_rows = df.count()
    columns = df.columns

    logging.info(f"Total rows in the DataFrame: {total_rows}")

    statistics = []

    for column in numeric_columns:
        if column not in df.columns:
            raise ValueError(
                f"Column '{column}' does not exist in the DataFrame."
            )

    for column in columns:
        logging.info(f"Processing column '{column}'")

        distinct_count = None
        min_value = None
        max_value = None

        if column not in numeric_columns:
            distinct_count = df.select(
                countDistinct(col(column)).alias('DistinctCount')
            ).collect()[0]['DistinctCount']

        null_count = df.filter(col(column).isNull()).count()

        null_percentage = (
            null_count / total_rows
        ) * 100 if total_rows > 0 else 0.0

        null_percentage = float(f"{null_percentage:.3f}")

        if column in numeric_columns:
            min_value = df.select(
                spark_min(column).alias('min')
            ).first()['min']
            max_value = df.select(
                spark_max(column).alias('max')
            ).first()['max']

        statistics.append(
            (
                column,
                distinct_count,
                null_count,
                null_percentage,
                min_value,
                max_value
            )
        )

    schema = StructType([
        StructField("Column", StringType(), True),
        StructField("DistinctCount", IntegerType(), True),
        StructField("NullCount", IntegerType(), True),
        StructField("NullPercentage", FloatType(), True),
        StructField("MinValue", StringType(), True),
        StructField("MaxValue", StringType(), True)
    ])

    statistics_df = df.sparkSession.createDataFrame(statistics, schema)

    logging.info(
        "Data Quality Check: Successfully processed standard analysis."
    )

    return statistics_df


def validate_column_patterns(
    df: DataFrame,
    patterns: dict
) -> DataFrame:
    """
    Validate columns in the DataFrame based on specified patterns.

    Args:
        df: Input DataFrame to perform validation.
        patterns:
            Dictionary with column names as keys
            and validation patterns as values.
                Example: {"CustomerRoute": "^BR\\d{4}$"}

    Returns:
        DataFrame: DataFrame with validation results containing:
            - Column: Name of the column.
            - TotalValid: Number of valid entries.
            - TotalInvalid: Number of invalid entries.
            - PercentValid: Percentage of valid entries.

    Raises:
        ValueError: If a specified column does not exist in the DataFrame.

    Examples:
        >>> from pyspark.sql import SparkSession
        >>> from pyspark.sql.types import StructType, StructField, StringType

        >>> spark = SparkSession.builder.getOrCreate()

        >>> schema = StructType([
        ...     StructField("CustomerRoute", StringType(), True),
        ...     StructField("OrderID", StringType(), True)
        ... ])

        >>> data = [
        ...         ("BR1234", "ORD001"),
        ...         ("BR5678", "ORD002"),
        ...         ("US9876", "ORD003")
        ... ]

        >>> df = spark.createDataFrame(data, schema)

        >>> patterns = {"CustomerRoute": "^BR\\d{4}$"}

        >>> try:
        ...     result_df = validate_column_patterns(df, patterns)
        ... except ValueError as e:
        ...     print(e)

        ***Logs:***

        - INFO: Processing column `CustomerRoute`
        - INFO: Valid entries in column `CustomerRoute: 2`
        - INFO: Invalid entries in column `CustomerRoute: 1`
        - INFO: Data Quality Check: Successfully processed pattern validation.
    """
    results = []

    for column, pattern in patterns.items():
        if column not in df.columns:
            raise ValueError(
                f"Column '{column}' does not exist in the DataFrame."
            )

        logging.info(f"Processing column '{column}'")

        non_null_df = df.filter(col(column).isNotNull())

        valid_count = non_null_df.filter(
            F.regexp_replace(col(column), pattern, "") == ""
        ).count()
        total_count = non_null_df.count()
        invalid_count = total_count - valid_count
        valid_percentage = (
            valid_count / total_count
        ) * 100 if total_count > 0 else 0.0
        valid_percentage = float(f"{valid_percentage:.3f}")

        logging.info(f"Valid entries in column '{column}': {valid_count}")
        logging.info(f"Invalid entries in column '{column}': {invalid_count}")

        results.append((column, valid_count, invalid_count, valid_percentage))

    schema = StructType([
        StructField("Column", StringType(), True),
        StructField("TotalValid", IntegerType(), True),
        StructField("TotalInvalid", IntegerType(), True),
        StructField("PercentValid", FloatType(), True)
    ])

    result_df = df.sparkSession.createDataFrame(results, schema)

    logging.info(
        "Data Quality Check: Successfully processed pattern validation."
    )

    return result_df


def get_distinct_values_as_list(
    df: DataFrame,
    columns: list
) -> DataFrame:
    """
    Retrieve distinct values for the provided columns
        and return a DataFrame with these values as lists.

    Args:
        df: Input DataFrame.
        columns: List of column names to get distinct values for.

    Returns:
        DataFrame: DataFrame containing:
            - Column:
                Name of the column.
            - DistinctValues:
                List of distinct values as a comma-separated string.

    Raises:
        ValueError:
            If any of the specified columns do not exist in the DataFrame.

    Examples:
        >>> from pyspark.sql import SparkSession
        >>> from pyspark.sql.types import StructType, StructField, StringType

        >>> spark = SparkSession.builder.getOrCreate()

        >>> schema = StructType([
        ...     StructField("Category", StringType(), True),
        ...     StructField("Region", StringType(), True)
        ... ])

        >>> data = [
        ...         ("Electronics", "North"),
        ...         ("Furniture", "South"),
        ...         ("Electronics", "West"),
        ...         ("Furniture", "North")
        ... ]

        >>> df = spark.createDataFrame(data, schema)

        >>> try:
        ...     result_df = get_distinct_values_as_list(
        ...         df, ["Category", "Region"]
        ...     )
        ... except ValueError as e:
        ...     print(e)

        ***Logs:***

        - INFO: Processing distinct values for column `Category`
        - INFO: Processing distinct values for column `Region`
        - INFO: Data Quality Check: Successfully retrieved distinct values.
    """

    schema = StructType([
        StructField("Column", StringType(), True),
        StructField("DistinctValues", StringType(), True)
    ])

    distinct_values = []

    for column in columns:
        if column not in df.columns:
            raise ValueError(
                f"Column '{column}' does not exist in the DataFrame."
            )

        logging.info(f"Processing distinct values for column '{column}'")

        distinct_list = df.select(
            column).distinct().rdd.flatMap(lambda x: x).collect()
        # Replace null values with 'null'
        cleaned_list = [
            str(value) if value is not None else 'null' for value in distinct_list  # noqa : E501
        ]

        distinct_values.append((column, ', '.join(cleaned_list)))

    result_df = df.sparkSession.createDataFrame(distinct_values, schema)

    logging.info(
        "Data Quality Check: Successfully retrieved distinct values."
    )

    return result_df


def plot_boxplots(
    df: DataFrame,
    columns: list
) -> None:
    """
    Plots boxplots for specified columns of a DataFrame using PySpark.

    Parameters:
        df: Input PySpark DataFrame to be plotted.
        columns: List of column names to plot.

    Returns:
        None: Displays the boxplots.

    Raises:
        ValueError: If any column in the list is not numeric.

    Examples:
        >>> from pyspark.sql import SparkSession
        >>> from pyspark.sql.types import StructType, StructField, IntegerType

        >>> spark = SparkSession.builder.getOrCreate()

        >>> schema = StructType([
        ...     StructField("id", IntegerType(), True),
        ...     StructField("score1", IntegerType(), True),
        ...     StructField("score2", IntegerType(), True)
        ... ])

        >>> data = [(1, 10, 15), (2, 15, 20), (3, 25, 30), (4, 5, 12)]

        >>> df = spark.createDataFrame(data, schema)

        >>> plot_boxplots(df, ["score1", "score2"])

        ***Logs:***

        - INFO: Plotting boxplot for column: `score1`
        - INFO: Plotting boxplot for column: `score2`
    """
    plt.figure(figsize=(15, 5))

    for i, column in enumerate(columns):
        if not isinstance(
            df.schema[column].dataType,
            (IntegerType, FloatType, DoubleType, DecimalType)
        ):
            raise ValueError(f"Column {column} is not numeric.")

        logging.info(f"Plotting boxplot for column: `{column}`")

        data = df.select(col(column)).rdd.flatMap(lambda x: x).collect()

        plt.subplot(1, len(columns), i + 1)
        sns.boxplot(x=data)
        plt.title(f'Boxplot of {column}')

    plt.tight_layout()
    plt.show()


def analyses_numeric_values(
    df: DataFrame,
    columns: list
) -> DataFrame:
    """
    Analyze numeric values in specified columns of a DataFrame.

    This function calculates the count of negative, zero, and positive values,
    along with the overall average for each specified column.

    Parameters:
        df:
            The input PySpark DataFrame.
        columns:
            List of column names to perform the count and average operations.

    Returns:
        DataFrame: A DataFrame with counts and averages for each column.

    Raises:
        ValueError: If any column in the list is not numeric.

    Examples:
        >>> from pyspark.sql import SparkSession
        >>> from pyspark.sql.types import StructType, StructField, IntegerType

        >>> spark = SparkSession.builder.getOrCreate()

        >>> schema = StructType([
        ...     StructField("id", IntegerType(), True),
        ...     StructField("score", IntegerType(), True)
        ... ])

        >>> data = [(1, -10), (2, 0), (3, 15), (4, -5), (5, 10)]

        >>> df = spark.createDataFrame(data, schema)

        >>> result_df = analyses_numeric_values(df, ["score"])

        ***Logs:***

        - INFO: Analyzing numeric values for column: `score`
    """

    results = []

    for column in columns:
        if not isinstance(
            df.schema[column].dataType, (
                IntegerType,
                FloatType,
                DoubleType,
                DecimalType
            )
        ):
            raise ValueError(f"Column '{column}' is not numeric.")

        logging.info(f"Analyzing numeric values for column: `{column}`")

        count_negative_values = df.filter(F.col(column) < 0).count()
        count_zero_values = df.filter(F.col(column) == 0).count()
        count_positive_values = df.filter(F.col(column) > 0).count()
        avg_overall = df.agg(
            F.avg(F.col(column)).alias("avg_overall")
        ).collect()[0]["avg_overall"]

        results.append(
            (
                column,
                count_negative_values,
                count_zero_values,
                count_positive_values,
                avg_overall
            )
        )

    schema = StructType([
        StructField("Column", StringType(), True),
        StructField("CountNegativeValues", IntegerType(), True),
        StructField("CountZeroValues", IntegerType(), True),
        StructField("CountPositiveValues", IntegerType(), True),
        StructField("AvgOverall", FloatType(), True)
    ])

    result_df = df.sparkSession.createDataFrame(results, schema)

    return result_df
