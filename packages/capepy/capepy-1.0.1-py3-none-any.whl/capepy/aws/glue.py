import sys
from typing import Optional

from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions
from pyspark.sql import SparkSession

from capepy.aws.meta import Boto3Object


class EtlJob(Boto3Object):
    """An object for creating ETL Jobs for use in AWS Glue

    Attributes:
        spark_ctx: The PySpark session
        glue_ctx: The AWS Glue context
        logger: The logger for logging to AWS Glue
        parameters: A dictionary of parameters passed into the job
    """

    def __init__(self):
        """Constructor for instantiating a new Glue ETL Job"""
        super().__init__()
        self.spark_ctx = SparkSession.builder.getOrCreate()  # pyright: ignore
        self.glue_ctx = GlueContext(self.spark_ctx)
        self.logger = self.glue_ctx.get_logger()
        self.parameters = getResolvedOptions(
            sys.argv,
            [
                "RAW_BUCKET_NAME",
                "OBJECT_KEY",
                "CLEAN_BUCKET_NAME",
            ],
        )

    def get_raw_file(self):
        """Retrieve the raw file from S3 and return its contents as a byte string.

        Raises:
            Exception: If the raw file is unable to be successfully retrieved from S3.

        Returns:
            A byte string of the raw file contents
        """
        response = self.get_client("s3").get_object(
            Bucket=self.parameters["RAW_BUCKET_NAME"],
            Key=self.parameters["OBJECT_KEY"],
        )
        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

        if status != 200:
            err = (
                f"ERROR - Could not get object {self.parameters['OBJECT_KEY']} from "
                f"bucket {self.parameters['RAW_BUCKET_NAME']}. ETL Cannot continue."
            )

            self.logger.error(err)

            # NOTE: need to properly handle exception stuff here, and we probably want
            #       this going somewhere very visible (e.g. SNS topic or a perpetual log
            #       as someone will need to be made aware)
            raise Exception(err)

        self.logger.info(
            f"Obtained object {self.parameters['OBJECT_KEY']} from bucket"
            f"{self.parameters['RAW_BUCKET_NAME']}"
        )

        return response.get("Body").read()

    def write_clean_file(self, clean_data, clean_key: Optional[str] = None):
        """Write data to a clean data file inside the clean S3 bucket as configured by the Glue ETL job.

        Args:
            clean_data (byes or seekable file-like object): Object data to be written to s3.
            clean_key: The prefix and filename for the new clean data file within the clean s3 bucket.

        Raises:
            Exception: If the clean data file is unable to be successfully put into s3.
        """
        response = self.get_client("s3").put_object(
            Bucket=self.parameters["CLEAN_BUCKET_NAME"],
            Key=clean_key,
            Body=clean_data,
        )

        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

        if status != 200:
            err = (
                f"ERROR - Could not write transformed data object {clean_key} "
                f"to bucket {self.parameters['CLEAN_BUCKET_NAME']}. ETL Cannot continue."
            )

            self.logger.error(err)

            # NOTE: need to properly handle exception stuff here, and we probably
            #       want this going somewhere very visible (e.g. SNS topic or a
            #       perpetual log as someone will need to be made aware)
            raise Exception(err)

        self.logger.info(
            f"Transformed {self.parameters['RAW_BUCKET_NAME']}/{self.parameters['OBJECT_KEY']} and wrote result "
            f"to {self.parameters['CLEAN_BUCKET_NAME']}/{clean_key}"
        )
