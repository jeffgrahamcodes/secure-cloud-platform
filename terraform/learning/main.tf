# Provider configuration
terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# S3 Bucket - Your first resource
resource "aws_s3_bucket" "learning_bucket" {
  bucket = "secure-platform-learning-${var.environment}-${random_id.bucket_suffix.hex}"

  tags = {
    Name        = "Learning Bucket"
    Environment = var.environment
    Project     = "secure-cloud-platform"
    ManagedBy   = "Terraform"
    Creator     = "Jeff Graham"
  }
}

# Random ID for unique bucket name
resource "random_id" "bucket_suffix" {
  byte_length = 4
}

# Enable versioning
resource "aws_s3_bucket_versioning" "learning_bucket_versioning" {
  bucket = aws_s3_bucket.learning_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}

# Enable encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "learning_bucket_encryption" {
  bucket = aws_s3_bucket.learning_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}