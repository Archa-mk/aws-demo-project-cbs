# gold_etl.py

import sys
import logging
import boto3
from datetime import datetime
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.sql.functions import sum as _sum


def run_gold_job():
    args = getResolvedOptions(sys.argv, ['JOB_NAME'])

    sc = SparkContext()
    glueContext = GlueContext(sc)
    spark = glueContext.spark_session
    job = Job(glueContext)
    job.init(args['JOB_NAME'], args)

    # ---- Logging Setup ----
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = f"/tmp/{args['JOB_NAME']}_{timestamp}.log"

    logger = logging.getLogger(args['JOB_NAME'])
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        fh = logging.FileHandler(log_file)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    s3 = boto3.client("s3")
    log_bucket = "financial-demo-sink-data"
    log_key = f"logs/gold/{args['JOB_NAME']}_{timestamp}.log"

    try:
        silver_path = "s3://financial-demo-sink-data/silver/facttransaction/"
        gold_path = "s3://financial-demo-sink-data/gold/facttransaction/"

        logger.info(f"Reading Silver layer from {silver_path}")
        df_silver = spark.read.parquet(silver_path)
        logger.info(f"Silver record count: {df_silver.count()}")

        logger.info("Aggregating Gold layer")
        df_gold = df_silver.groupBy("transaction_date") \
                          .agg(_sum("transaction_amount").alias("total_transaction_amount"))
        logger.info(f"Gold record count: {df_gold.count()}")

        logger.info(f"Writing Gold layer to {gold_path}")
        df_gold.write.mode("overwrite").parquet(gold_path)
        logger.info("Gold ETL completed successfully")

        job.commit()
        logger.info("Glue job committed successfully")

    except Exception:
        logger.error("Gold ETL failed", exc_info=True)
        raise

    finally:
        try:
            s3.upload_file(log_file, log_bucket, log_key)
            logger.info(f"Logs uploaded to s3://{log_bucket}/{log_key}")
        except Exception as e:
            print(f"Log upload failed: {str(e)}")


if __name__ == "__main__":
    run_gold_job()