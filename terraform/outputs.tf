output "state_machine_arn" {
  value = aws_sfn_state_machine.etl_workflow.arn
}

output "bronze_job_name" {
  value = aws_glue_job.bronze_job.name
}