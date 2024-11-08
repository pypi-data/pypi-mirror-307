import logging
import os
from typing import List

import boto3
import pyspark.sql.functions as F
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, lit
from sws_api_client import Tags
from sws_api_client.tags import DisseminatedTag

from .constants import DomainFilters


def get_spark() -> SparkSession:
    session = boto3.session.Session()
    credentials = session.get_credentials()

    aws_access_key_id = credentials.access_key
    aws_secret_access_key = credentials.secret_key
    session_token = credentials.token

    # get EMR_BUCKET from environment variable
    emr_bucket = os.getenv("EMR_BUCKET")
    output_path = f"s3://{emr_bucket}"

    spark = (
        SparkSession.builder.appName("Spark-on-AWS-Lambda")
        .config("spark.hadoop.fs.s3a.access.key", aws_access_key_id)
        .config("spark.hadoop.fs.s3a.secret.key", aws_secret_access_key)
        .config("spark.hadoop.fs.s3a.session.token", session_token)
        .config(
            "spark.hadoop.fs.s3a.aws.credentials.provider",
            "org.apache.hadoop.fs.s3a.TemporaryAWSCredentialsProvider",
        )
        .config(
            "spark.hadoop.hive.metastore.client.factory.class",
            "com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory",
        )
        .config("spark.jars.packages", "org.apache.iceberg")
        .config(
            "spark.sql.extensions",
            "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions",
        )
        .config(
            "spark.sql.catalog.AwsDataCatalog",
            "org.apache.iceberg.spark.SparkCatalog",
        )
        .config(
            "spark.sql.catalog.AwsDataCatalog.catalog-impl",
            "org.apache.iceberg.aws.glue.GlueCatalog",
        )
        .config("spark.sql.catalog.AwsDataCatalog.warehouse", output_path)
        .config("spark.sql.defaultCatalog", "AwsDataCatalog")
        .enableHiveSupport()
        .getOrCreate()
    )

    return spark


def check_mappings(
    column_mappings: List[str], columns: List[str], table_name: str
) -> None:
    column_mappings_set = set(column_mappings)
    columns_set = set(columns)

    if not (columns_set <= column_mappings_set):
        missing_mappings = columns_set - column_mappings_set

        message = f'There mappings in the table "{table_name}" are not correct'
        message += f"\nThe following column mappings are missing: {missing_mappings}"

        raise ValueError(message)


def map_codes(
    df: DataFrame,
    df_mapping: DataFrame,
    domain_code: str,
    col_name: str,
    col_type: str,
    src_column: str,
    dest_column: str,
) -> DataFrame:
    return (
        df.alias("d")
        # Join the data with the standard mapping for the specific dimension
        .join(
            F.broadcast(
                df_mapping.filter(
                    (col("domain").isNull() | (col("domain") == lit("")))
                    & (col("var_type") == lit(col_type))
                    & (
                        col("mapping_type").isNull()
                        | (col("mapping_type").isNull() == lit(""))
                    )
                )
            ).alias("m_standard"),
            col(f"d.{col_name}") == col(f"m_standard.{src_column}"),
            "left",
        )
        # Join the data with the domain specific mapping for the specific dimension
        .join(
            F.broadcast(
                df_mapping.filter(
                    (col("domain") == lit(domain_code))
                    & (col("var_type") == lit(col_type))
                    & (
                        col("mapping_type").isNull()
                        | (col("mapping_type").isNull() == lit(""))
                    )
                )
            ).alias("m_domain"),
            col(f"d.{col_name}") == col(f"m_domain.{src_column}"),
            "left",
        )
        # Select only the columns we are interested in (this step is optional but recommended for debugging)
        .select(
            "d.*",
            col(f"m_standard.{dest_column}").alias(f"standard_{dest_column}"),
            col("m_standard.delete").alias("standard_delete"),
            col("m_standard.multiplier").alias("standard_multiplier"),
            col(f"m_domain.{dest_column}").alias(f"domain_specific_{dest_column}"),
            col("m_domain.delete").alias("domain_specific_delete"),
            col("m_domain.multiplier").alias("domain_specific_multiplier"),
        )
        # Filter out records to delete
        .filter(
            # Evaluate first the domain specific flag
            F.when(
                col("domain_specific_delete").isNotNull(),
                ~col("domain_specific_delete"),
            )
            # Then evaluate the general flag
            .when(
                col("standard_delete").isNotNull(), ~col("standard_delete")
            ).otherwise(lit(True))
        )
        .withColumn(
            col_name,
            # Evaluate first the domain specific mapping
            F.when(
                col(f"domain_specific_{dest_column}").isNotNull(),
                col(f"domain_specific_{dest_column}"),
            )
            # Then evaluate the general mapping
            .when(
                col(f"standard_{dest_column}").isNotNull(),
                col(f"standard_{dest_column}"),
            ).otherwise(col(col_name)),
        )
        .withColumn(
            "value",
            # Multiply first by the domain specific multiplier
            F.when(
                col("domain_specific_multiplier").isNotNull(),
                col("value") * col("domain_specific_multiplier"),
            )
            # Then multiply by the general multiplier
            .when(
                col(f"standard_{dest_column}").isNotNull(),
                col("value") * col("standard_multiplier"),
            ).otherwise(col("value")),
        )
        # Remove the columns that were not in the original dataset
        .drop(
            f"standard_{dest_column}",
            "standard_delete",
            "standard_multiplier",
            f"domain_specific_{dest_column}",
            "domain_specific_delete",
            "domain_specific_multiplier",
        )
    )


def apply_code_correction(
    df: DataFrame,
    df_mapping_code_correction: DataFrame,
    domain_code: str,
    col_name: str,
    col_type: str,
) -> DataFrame:
    logging.info(f"correcting codes for column {col_name} of type {col_type}")
    return map_codes(
        df,
        df_mapping_code_correction,
        domain_code,
        col_name,
        col_type,
        src_column="old_code",
        dest_column="new_code",
    )


def copy_cache_csv_dataset_to_tag(
    bucket: str,
    prefix: str,
    tag_name: str,
) -> None:

    logging.info(
        f"Copying the source folder '{prefix}latest/' to '{prefix}{tag_name}/'"
    )

    s3 = boto3.client("s3")

    source_prefix = f"{prefix}latest/"

    response = s3.list_objects_v2(Bucket=bucket, Prefix=source_prefix)

    s3_paths = [content["Key"] for content in response.get("Contents", {})]

    logging.debug("list_objects_v2 response:")
    logging.debug(response)
    logging.debug("objects to copy:")
    logging.debug(s3_paths)

    for s3_path in s3_paths:
        result = s3.copy_object(
            Bucket=bucket,
            CopySource={"Bucket": bucket, "Key": s3_path},
            Key=f"{s3_path.replace('latest', tag_name)}",
        )
        logging.info(result)


def save_cache_csv(df: DataFrame, bucket: str, prefix: str, tag_name: str) -> None:

    s3 = boto3.client("s3")

    latest_path = f"s3://{bucket}/{prefix}/latest"
    tag_path = f"s3://{bucket}/{prefix}/{tag_name}"

    latest_prefix = f"{prefix}/latest"
    tag_prefix = f"{prefix}/{tag_name}"

    s3.delete_object(Bucket=bucket, Key=f"{latest_prefix}.csv")
    df.coalesce(1).write.option("header", True).mode("overwrite").csv(latest_path)

    response = s3.list_objects_v2(Bucket=bucket, Prefix=latest_prefix)

    s3_path_objects_keys = [content["Key"] for content in response.get("Contents", {})]
    s3_path_csv = [
        s3_object for s3_object in s3_path_objects_keys if s3_object.endswith(".csv")
    ][0]

    # Extract the csv from the folder and delete the folder
    result_latest = s3.copy_object(
        Bucket=bucket,
        CopySource={"Bucket": bucket, "Key": s3_path_csv},
        Key=f"{latest_prefix}.csv",
    )
    logging.info(f"Updated latest version of cached csv at {latest_path}.csv")

    result_tag = s3.copy_object(
        Bucket=bucket,
        CopySource={"Bucket": bucket, "Key": s3_path_csv},
        Key=f"{tag_prefix}.csv",
    )
    logging.info(f"Wrote the tag version of cached csv at {tag_path}.csv")

    for object in s3_path_objects_keys:
        s3.delete_object(Bucket=bucket, Key=object)
    logging.debug("Cleaning the temporary folder of the csv files")


def create_table_if_not_exists_otherwise_replace(
    spark: SparkSession, df: DataFrame, table_name: str
):
    table_exists = spark.catalog.tableExists(table_name)

    if not table_exists:
        df.writeTo(table_name).createOrReplace()
    else:
        spark.sql(f"DELETE FROM {table_name} WHERE true")
        df.writeTo(table_name).append()


def correct_domain_filter(
    df: DataFrame, domain: str, unique_columns: List[str]
) -> DataFrame:
    ordered_columns = df.columns

    # Filter for domain entries
    df_domain = df.filter(DomainFilters.MATCH(domain))

    # Filter for empty domain entries
    df_empty = df.filter(DomainFilters.EMPTY())

    # Get the difference: empty domains that are not in the domain entries
    df_empty_diff = df_empty.join(df_domain, unique_columns, "left_anti").select(
        *ordered_columns
    )

    # Combine the domain entries with the non-matching empty entries
    df_final = df_domain.union(df_empty_diff)

    return df_final


def check_duplicates_in_df(
    df: DataFrame,
    table_name: str,
    unique_columns: List[str],
) -> DataFrame:
    duplicated_values = (
        df.groupBy(*unique_columns)
        .count()
        .filter(col("count") > 1)
        .select(*unique_columns)
        .collect()
    )

    if len(duplicated_values) > 0:
        raise RuntimeError(
            f"There are the following duplicated values in the table {table_name} for the columns {str(unique_columns)}: {str(duplicated_values)}"
        )

    return df


# SWS metadata Tags management


# Function to get or create a tag
def get_or_create_tag(
    tags: Tags, dataset: str, tag_id: str, name: str, description: str = ""
):
    try:
        tag = tags.get_disseminated_tag(dataset, tag_id)
        if tag is None:
            raise Exception("Tag not found")
        logging.info(f"Tag found")
        logging.debug(f"Tag found: {tag}")
    except Exception as e:
        logging.info(f"Tag not found: {e}. Creating new tag.")
        tag = tags.create_disseminated_tag(dataset, name, tag_id, description)
    return tag


# Function to check if a table exists in the tag
def table_exists(tag: DisseminatedTag, table_name):
    for table in tag.get("tables"):
        if table["name"] == table_name:
            return True
    return False


# Function to check if a dissemination step exists in the tag
def step_exists(tag, target, table_id):
    for step in tag["disseminationSteps"]:
        if step["target"] == target and step["table"] == table_id:
            return True
    return False
