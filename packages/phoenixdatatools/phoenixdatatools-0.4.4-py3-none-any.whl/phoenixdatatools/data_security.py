import logging

from cryptography.fernet import Fernet
from pyspark.sql import DataFrame
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType


def generate_encryption_key() -> bytes:
    """
    Generates a new encryption key using Fernet.

    Returns:
        bytes: The encryption key.

    Examples:
        >>> key = generate_encryption_key()
        >>> isinstance(key, bytes)
        True

        ***Logs:***

        - INFO: Encryption Key generated successfully.
    """
    key = Fernet.generate_key()
    logging.info("Encryption Key generated successfully.")
    return key


def encrypt_dataframe(
    data_frame: DataFrame,
    columns_to_encrypt: list,
    key: bytes
) -> DataFrame:
    """
    Encrypts specified columns in a DataFrame using the provided key.

    Args:
        data_frame: Input DataFrame with data to be encrypted.
        columns_to_encrypt: List of column names to encrypt.
        key: Encryption key to use for encryption.

    Returns:
        DataFrame: A DataFrame with encrypted columns.

    Raises:
        Exception:
            If any of the columns to encrypt are not found in the DataFrame.

    Examples:
        >>> from pyspark.sql import SparkSession
        >>> from pyspark.sql.types import StructType, StructField, StringType
        >>> spark = SparkSession.builder.getOrCreate()

        >>> schema = StructType([
        ...     StructField("id", StringType(), True),
        ...     StructField("name", StringType(), True)
        ... ])

        >>> data = [("1", "Alice"), ("2", "Bob")]

        >>> df = spark.createDataFrame(data, schema)
        >>> key = generate_encryption_key()
        >>> encrypted_df = encrypt_dataframe(df, ["name"], key)

        ***Logs:***

        - ERROR: Encryption Failed: `column` is not present in the DataFrame!

        - INFO: DataFrame columns `columns_to_encrypt` encrypted successfully.
    """
    encrypt_udf = udf(
        lambda value: Fernet(
            key).encrypt(value.encode()).decode(), StringType()
    )

    for column in columns_to_encrypt:
        if column not in data_frame.columns:
            raise Exception(
                f"Encryption Failed: {column} is not present in the DataFrame!"
            )

        data_frame = data_frame.withColumn(
            column, encrypt_udf(data_frame[column])
        )

    logging.info(
        f"DataFrame columns {columns_to_encrypt} encrypted successfully."
    )

    return data_frame


def decrypt_dataframe(
    data_frame: DataFrame,
    columns_to_decrypt: list,
    key: bytes
) -> DataFrame:
    """
    Decrypts specified columns in a DataFrame using the provided key.

    Args:
        data_frame: Input DataFrame with data to be decrypted.
        columns_to_decrypt: List of column names to decrypt.
        key: Decryption key to use for decryption.

    Returns:
        DataFrame: A DataFrame with decrypted columns.

    Raises:
        Exception:
            If any of the columns to decrypt are not found in the DataFrame.

    Examples:
        >>> from pyspark.sql import SparkSession
        >>> from pyspark.sql.types import StructType, StructField, StringType
        >>> spark = SparkSession.builder.getOrCreate()

        >>> schema = StructType([
        ...     StructField("id", StringType(), True),
        ...     StructField("name", StringType(), True)
        ... ])

        >>> data = [("1", "gAAAAABg0f8JqXc2..."), ("2", "gAAAAABg0f8JqXc2...")]

        >>> df = spark.createDataFrame(data, schema)
        >>> key = generate_encryption_key()
        >>> decrypted_df = decrypt_dataframe(df, ["name"], key)

        ***Logs:***

        - ERROR: Decryption Failed: `column` is not present in the DataFrame!

        - INFO: DataFrame columns `columns_to_decrypt` decrypted successfully.
    """
    decrypt_udf = udf(
        lambda value: Fernet(
            key).decrypt(value.encode()).decode(), StringType()
    )

    for column in columns_to_decrypt:
        if column not in data_frame.columns:
            raise Exception(
                f"Decryption Failed: {column} is not present in the DataFrame!"
            )

        data_frame = data_frame.withColumn(
            column, decrypt_udf(data_frame[column])
        )

    logging.info(
        f"DataFrame columns {columns_to_decrypt} decrypted successfully."
    )

    return data_frame
