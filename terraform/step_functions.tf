resource "aws_sfn_state_machine" "etl_workflow" {
  name     = "financial-etl-workflow"
  role_arn = aws_iam_role.step_function_role.arn

  definition = jsonencode({
    Comment = "Bronze-Silver-Gold ETL Workflow",
    StartAt = "BronzeJob",
    States = {
      BronzeJob = {
        Type     = "Task",
        Resource = "arn:aws:states:::glue:startJobRun.sync",
        Parameters = {
          JobName = aws_glue_job.bronze_job.name
        },
        Next = "SilverJob"
      },
      SilverJob = {
        Type     = "Task",
        Resource = "arn:aws:states:::glue:startJobRun.sync",
        Parameters = {
          JobName = aws_glue_job.silver_job.name
        },
        Next = "GoldJob"
      },
      GoldJob = {
        Type     = "Task",
        Resource = "arn:aws:states:::glue:startJobRun.sync",
        Parameters = {
          JobName = aws_glue_job.gold_job.name
        },
        End = true
      }
    }
  })
}