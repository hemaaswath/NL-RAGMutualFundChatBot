# RAG Mutual Fund FAQ Assistant - Deployment Guide

This document provides comprehensive deployment instructions for the RAG Mutual Fund FAQ Assistant.

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
- [CI/CD Pipeline](#cicd-pipeline)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)

## Overview

The RAG Mutual Fund FAQ Assistant consists of:
- **Phase 1**: Data Collection (HTML parsing, chunking, embeddings, vector store)
- **Phase 2**: RAG Pipeline (retrieval, generation, refusal handling)
- **Phase 3**: Backend API (FastAPI REST API)
- **Phase 4**: Frontend UI (Streamlit-based interface)
- **Phase 5**: Testing & Quality Assurance
- **Phase 6**: Deployment & Documentation

## Prerequisites

### Local Development
- Python 3.11+
- pip
- Git
- GROQ API key

### Docker Deployment
- Docker 20.10+
- Docker Compose 2.0+

### Cloud Deployment
- AWS account
- Terraform 1.0+
- AWS CLI configured
- Docker installed

## Local Development

### 1. Clone the Repository
```bash
git clone https://github.com/your-org/RAG-MutualFund-ChatBot.git
cd RAG-MutualFund-ChatBot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env with your GROQ_API_KEY
```

### 4. Run Phase 1 (Data Collection)
```bash
python Docs/src/phase1/main.py
```

### 5. Run Backend API
```bash
python run_api.py
```

### 6. Run Frontend UI
```bash
python run_ui.py
```

### 7. Run Tests
```bash
# Run all tests
python Tests/Phase5/run_tests.py

# Run specific phase tests
python Tests/Phase1/run_tests.py
python Tests/Phase2/run_tests.py
python Tests/Phase3/run_tests.py
```

## Docker Deployment

### Using Docker Compose (Recommended for Local)

```bash
cd Docs/Deployment/6.1_containerization
docker-compose up -d
```

Services will be available at:
- Backend API: http://localhost:8000
- Frontend UI: http://localhost:8501
- API Docs: http://localhost:8000/docs

### Using Individual Dockerfiles

#### Build Backend Image
```bash
docker build -f Docs/Deployment/6.1_containerization/Dockerfile.backend -t rag-backend .
```

#### Build Frontend Image
```bash
docker build -f Docs/Deployment/6.1_containerization/Dockerfile.frontend -t rag-frontend .
```

#### Run Containers
```bash
# Backend
docker run -p 8000:8000 -e GROQ_API_KEY=your_key rag-backend

# Frontend
docker run -p 8501:8501 rag-frontend
```

## Cloud Deployment

### AWS Deployment Using Terraform

#### 1. Configure AWS Credentials
```bash
aws configure
```

#### 2. Initialize Terraform
```bash
cd Docs/Deployment/6.2_cloud_infrastructure
terraform init
```

#### 3. Review Plan
```bash
terraform plan -var-file=terraform.tfvars
```

#### 4. Deploy Infrastructure
```bash
terraform apply -var-file=terraform.tfvars
```

#### 5. Get Load Balancer DNS
```bash
terraform output load_balancer_dns
```

### Deploy to ECR

#### 1. Login to ECR
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com
```

#### 2. Build and Push Images
```bash
# Backend
docker build -f Docs/Deployment/6.1_containerization/Dockerfile.backend -t 123456789012.dkr.ecr.us-east-1.amazonaws.com/rag-backend:latest .
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/rag-backend:latest

# Frontend
docker build -f Docs/Deployment/6.1_containerization/Dockerfile.frontend -t 123456789012.dkr.ecr.us-east-1.amazonaws.com/rag-frontend:latest .
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/rag-frontend:latest
```

## CI/CD Pipeline

### GitHub Actions

The project uses GitHub Actions for CI/CD:

- **CI Pipeline** (`.github/workflows/ci.yml`): Runs on every push and PR
  - Linting (Black, isort, Flake8)
  - Tests for all phases
  
- **CD Pipeline** (`.github/workflows/cd.yml`): Runs on main branch
  - Builds Docker images
  - Pushes to ECR
  - Deploys to ECS (staging/production)

### Manual Deployment

1. Ensure all tests pass
2. Merge to main branch
3. CD pipeline automatically deploys to production
4. Monitor deployment via AWS ECS console

## Monitoring

### Health Checks

- **Backend Health**: `GET /api/health`
- **Frontend Health**: `GET /_stcore/health`

### Logs

- **Local**: Check console output
- **Docker**: `docker-compose logs -f`
- **AWS**: CloudWatch Logs in ECS console

### Metrics

Track the following metrics:
- Response time (target: <3s for 90th percentile)
- Error rate (target: <1%)
- Cache hit rate (target: >70%)
- CPU/Memory usage

## Troubleshooting

### Common Issues

**Issue**: API returns 500 error
- **Solution**: Check GROQ_API_KEY is set correctly

**Issue**: Docker container fails to start
- **Solution**: Check port conflicts, ensure ports 8000 and 8501 are available

**Issue**: Terraform apply fails
- **Solution**: Check AWS credentials, ensure sufficient permissions

**Issue**: Tests fail in CI/CD
- **Solution**: Check test results artifact in GitHub Actions

### Getting Help

- Check logs in CloudWatch
- Review GitHub Actions workflow runs
- Check ECS task logs
- Review Terraform state

## Security Considerations

- Never commit `.env` files to version control
- Use AWS Secrets Manager for sensitive data
- Enable SSL/TLS for production deployments
- Regularly update dependencies
- Use least-privilege IAM policies

## Cost Optimization

- Use ECS Fargate Spot instances for non-critical workloads
- Enable CloudWatch Logs retention (7 days)
- Use AWS Graviton instances for cost savings
- Implement auto-scaling policies
