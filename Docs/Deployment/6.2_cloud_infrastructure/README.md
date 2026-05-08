# Cloud Infrastructure Setup

This directory contains Terraform configurations for deploying the RAG Mutual Fund ChatBot to AWS.

## Prerequisites
- Terraform >= 1.0
- AWS CLI configured with appropriate credentials
- AWS account with permissions to create resources

## Usage

1. Initialize Terraform:
```bash
terraform init
```

2. Plan the deployment:
```bash
terraform plan -var-file=terraform.tfvars
```

3. Apply the configuration:
```bash
terraform apply -var-file=terraform.tfvars
```

4. Destroy resources when needed:
```bash
terraform destroy -var-file=terraform.tfvars
```

## Infrastructure Components
- **VPC**: Virtual Private Cloud with public and private subnets
- **ECS**: Elastic Container Service for running Docker containers
- **ECS Fargate**: Serverless compute for backend and frontend
- **Application Load Balancer**: Load balancing and SSL termination
- **CloudWatch**: Logging and monitoring
- **Secrets Manager**: Secure storage for API keys

## Variables
Create a `terraform.tfvars` file to override default variables:
```hcl
project_name = "rag-mutual-fund"
environment = "production"
aws_region = "us-east-1"
groq_api_key = "your_groq_api_key_here"
```

## Cost Considerations
- ECS Fargate: Pay per vCPU and memory per hour
- Load Balancer: ~$0.025 per hour
- CloudWatch Logs: ~$0.50 per GB ingested
- Secrets Manager: ~$0.40 per secret per month

## Security
- All resources are tagged with project name and environment
- Security groups follow least privilege principle
- API keys stored in AWS Secrets Manager
- Private subnets for backend services
