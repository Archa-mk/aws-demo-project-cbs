data "aws_iam_role" "glue_role" {
  name = "practical-demo-role"
}

resource "aws_glue_job" "bronze_job" {
  name     = "bronze-etl-job"
  role_arn = data.aws_iam_role.glue_role.arn

  command {
    script_location = "s3://${var.script_bucket}/bronze_etl.py"
    python_version  = "3"
  }

  glue_version      = "4.0"
  worker_type       = "G.1X"
  number_of_workers = 2
}

resource "aws_glue_job" "silver_job" {
  name     = "silver-etl-job"
  role_arn = data.aws_iam_role.glue_role.arn

  command {
    script_location = "s3://${var.script_bucket}/silver_etl.py"
    python_version  = "3"
  }

  glue_version      = "4.0"
  worker_type       = "G.1X"
  number_of_workers = 2
}

resource "aws_glue_job" "gold_job" {
  name     = "gold-etl-job"
  role_arn = data.aws_iam_role.glue_role.arn

  command {
    script_location = "s3://${var.script_bucket}/gold_etl.py"
    python_version  = "3"
  }

  glue_version      = "4.0"
  worker_type       = "G.1X"
  number_of_workers = 2
}