# Infrastructure (infra/)

IaC for Visitor on AWS (PRD §6, §8.2, §11). VIS-1 provides minimal stubs;
real resources/backends are provisioned per environment.

Components: VPC, RDS PostgreSQL, compute (ECS/Fargate), S3 (uploaded files),
Secrets Manager/SSM, ACM (TLS) + domains. Backups: RDS automated snapshots,
S3 versioning, repo backups.

```bash
terraform init
terraform plan  -var-file=env/dev.tfvars
terraform apply -var-file=env/dev.tfvars
```
