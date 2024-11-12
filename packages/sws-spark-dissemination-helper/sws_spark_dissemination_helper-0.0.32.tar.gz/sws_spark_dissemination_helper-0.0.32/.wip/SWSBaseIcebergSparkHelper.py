import logging
from copy import copy
from typing import List, Tuple

import pyspark.sql.functions as F
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, lit
from sws_api_client import Tags
from sws_api_client.tags import BaseDisseminatedTagTable, TableLayer, TableType

from .constants import IcebergDatabases, IcebergTables, IcebergTable
from .SWSPostgresSparkReader import SWSPostgresSparkReader
from .utils import get_or_create_tag, save_cache_csv
import boto3


class SWSBaseIcebergSparkHelper:

    def _write_to_iceberg(
        self,
        df: DataFrame,
        iceberg_table: IcebergTable,
        tag_name: str,
    ) -> DataFrame:
        # Write to Iceberg
        df.writeTo(iceberg_table.iceberg_id).createOrReplace()
        logging.info(f"Table written to {iceberg_table.iceberg_id}")

        # Create a tag in Iceberg if required
        self.spark.sql(
            f"ALTER TABLE {iceberg_table.iceberg_id} CREATE TAG `{tag_name}`"
        )
        logging.info(f"Tag '{tag_name}' created for {iceberg_table.iceberg_id}")

        return df

    def _write_to_csv(
        self, df: DataFrame, iceberg_table: IcebergTable, bucket: str, tag_name: str
    ) -> DataFrame:
        s3 = boto3.client("s3")

        latest_path = f"s3://{bucket}/{iceberg_table.csv_prefix}/latest"
        tag_path = f"s3://{bucket}/{iceberg_table.csv_prefix}/{tag_name}"

        latest_prefix = f"{iceberg_table.csv_prefix}/latest"
        tag_prefix = f"{iceberg_table.csv_prefix}/{tag_name}"

        s3.delete_object(Bucket=bucket, Key=f"{latest_prefix}.csv")
        df.coalesce(1).write.option("header", True).mode("overwrite").csv(latest_path)

        response = s3.list_objects_v2(Bucket=bucket, Prefix=latest_prefix)

        s3_path_objects_keys = [
            content["Key"] for content in response.get("Contents", {})
        ]
        s3_path_csv = [
            s3_object
            for s3_object in s3_path_objects_keys
            if s3_object.endswith(".csv")
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

        return df

    def _create_dissemination_tag(
        self,
        df: DataFrame,
        tags: Tags,
        iceberg_table: IcebergTable,
        level: str,
        domain_code: str,
        iceberg_description: str,
        csv_description: str,
    ) -> Tags:
        tag = get_or_create_tag(tags, self.dataset_id, self.tag_name, self.tag_name)
        logging.debug(f"Initial Tag: {tag}")

        # Common table structure
        base_table_structure = {
            "layer": level,
            "private": True,
            "structure": {"columns": df.schema.jsonValue()["fields"]},
        }

        # Add Iceberg table to tag
        iceberg_table = BaseDisseminatedTagTable(
            id=f"{domain_code}_{iceberg_table.level}_iceberg",
            name=f"{domain_code} {iceberg_table.level} Iceberg",
            description=iceberg_description,
            type=TableType.ICEBERG,
            database=iceberg_table.database,
            table=iceberg_table.table,
            path=iceberg_table.path,
            **base_table_structure,
        )
        tags.add_dissemination_table(self.dataset_id, self.tag_name, iceberg_table)
        logging.debug(f"Tag with added Iceberg Table: {tag}")

        # Add CSV table to tag
        csv_table = BaseDisseminatedTagTable(
            id=f"{domain_code}_{iceberg_table.level}_csv",
            name=f"{domain_code} {iceberg_table.level} CSV",
            description=csv_description,
            type=TableType.CSV,
            path=iceberg_table.csv_path,
            **base_table_structure,
        )
        tags.add_dissemination_table(self.dataset_id, self.tag_name, csv_table)
        logging.debug(f"Tag with added CSV Table: {tag}")

        return tag
