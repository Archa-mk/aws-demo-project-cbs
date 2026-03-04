# bronze_etl.py
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
import sys

args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

df_raw = spark.read.option("header", "true") \
    .option("inferSchema", "true") \
    .csv("s3://financial-demo-source-data/fact-transaction/")

df_raw.write.mode("overwrite") \
    .parquet("s3://financial-demo-sink-data/bronze/facttransaction/")

job.commit()