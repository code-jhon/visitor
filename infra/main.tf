# Visitor infrastructure (VIS-1 scaffolding stub).
# Real modules (VPC, RDS PostgreSQL, ECS/Fargate, S3, Secrets Manager, ACM)
# are added incrementally. Keep environments isolated via separate backends
# and *.tfvars (env/dev, env/staging, env/prod).

terraform {
  required_version = ">= 1.5.0"
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
