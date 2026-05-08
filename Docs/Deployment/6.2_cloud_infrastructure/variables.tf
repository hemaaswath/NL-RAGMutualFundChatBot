# Terraform variables
variable "project_name" {
  description = "Project name for resource tagging"
  type        = string
  default     = "rag-mutual-fund"
}

variable "environment" {
  description = "Environment (dev, staging, production)"
  type        = string
  default     = "dev"
}

variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "us-east-1"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

variable "backend_cpu" {
  description = "CPU units for backend ECS task"
  type        = number
  default     = 512
}

variable "backend_memory" {
  description = "Memory for backend ECS task (in MB)"
  type        = number
  default     = 1024
}

variable "backend_desired_count" {
  description = "Desired count of backend tasks"
  type        = number
  default     = 2
}

variable "ecr_repository_url" {
  description = "ECR repository URL for Docker images"
  type        = string
  default     = "123456789012.dkr.ecr.us-east-1.amazonaws.com/rag-mutual-fund"
}

variable "groq_api_key" {
  description = "Groq API key for LLM"
  type        = string
  sensitive   = true
}
