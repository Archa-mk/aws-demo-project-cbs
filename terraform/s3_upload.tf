resource "aws_s3_bucket_object" "bronze_script" {
  bucket = var.script_bucket
  key    = "bronze_etl.py"
  source = "../glue/bronze_etl.py"
  etag   = filemd5("../glue/bronze_etl.py")
}

resource "aws_s3_bucket_object" "silver_script" {
  bucket = var.script_bucket
  key    = "silver_etl.py"
  source = "../glue/silver_etl.py"
  etag   = filemd5("../glue/silver_etl.py")
}

resource "aws_s3_bucket_object" "gold_script" {
  bucket = var.script_bucket
  key    = "gold_etl.py"
  source = "../glue/gold_etl.py"
  etag   = filemd5("../glue/gold_etl.py")
}