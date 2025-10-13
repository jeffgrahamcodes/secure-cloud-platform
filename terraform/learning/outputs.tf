output "bucket_name" {
  description = "Name of the S3 bucket"
  value       = aws_s3_bucket.learning_bucket.id
}

output "bucket_arn" {
  description = "ARN of the S3 bucket"
  value       = aws_s3_bucket.learning_bucket.arn
}

output "bucket_region" {
  description = "Region of the S3 bucket"
  value       = aws_s3_bucket.learning_bucket.region
}