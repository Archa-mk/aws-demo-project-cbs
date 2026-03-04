# silver_etl.py
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.sql.functions import col, to_timestamp
import sys

args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

df_bronze = spark.read.parquet(
    "s3://financial-demo-sink-data/bronze/facttransaction/"
)

df_silver = df_bronze.dropna() \
    .withColumn("transaction_date",
                to_timestamp(col("TransactionDate"), "M/d/yyyy")) \
    .select(
        col("TransactionID").alias("transaction_id"),
        col("transaction_date"),
        col("TransactionAmount").alias("transaction_amount")
    ) \
    .dropDuplicates(["transaction_id"])

df_silver.write.mode("overwrite") \
    .parquet("s3://financial-demo-sink-data/silver/facttransaction/")

job.commit()