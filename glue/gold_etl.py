# gold_etl.py
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.sql.functions import sum as _sum
import sys

args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

df_silver = spark.read.parquet(
    "s3://financial-demo-sink-data/silver/facttransaction/"
)

df_gold = df_silver.groupBy("transaction_date") \
    .agg(_sum("transaction_amount")
         .alias("total_transaction_amount"))

df_gold.write.mode("overwrite") \
    .parquet("s3://financial-demo-sink-data/gold/facttransaction/")

job.commit()