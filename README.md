# Secure Cloud Platform

A production-ready microservices platform on AWS EKS demonstrating DevSecOps best practices.

## Project Goals

Build a secure, scalable cloud-native platform that showcases:

- **Infrastructure as Code** with Terraform
- **Container orchestration** with Kubernetes (EKS)
- **Security automation** with scanning and policy enforcement
- **CI/CD pipelines** with automated testing and deployment
- **Observability** with monitoring and logging

## Architecture

### Services

- **API Service** - Node.js REST API (Port 3000)
- **Auth Service** - JWT-based authentication (Port 3001)
- **Worker Service** - Python background job processing (Port 3002)

### Infrastructure

- AWS EKS for Kubernetes orchestration
- Terraform for infrastructure provisioning
- GitHub Actions for CI/CD (coming soon)
- Container security scanning with Trivy (coming soon)
- Network policies and RBAC (coming soon)

## Tech Stack

- **Languages:** Node.js, Python
- **Infrastructure:** Terraform, AWS (EKS, VPC, ECR)
- **Containers:** Docker, Kubernetes
- **CI/CD:** GitHub Actions
- **Security:** Trivy, Checkov, AWS Security Hub
- **Monitoring:** Prometheus, Grafana (planned)

## Roadmap

- [x] Project initialization
- [x] Week 1: Build API service with Docker
- [x] Week 1: Build Auth service with JWT
- [x] Week 1: Build Worker service with Python
- [x] Week 1: Deploy API service to Kubernetes
- [x] Week 1: Deploy all services to Kubernetes
- [x] Week 1: Service-to-service communication in K8s
- [x] Week 2: Terraform EKS infrastructure
- [x] Week 2: Deploy to AWS EKS (production environment)
- [ ] Week 3: CI/CD pipeline with security scanning
- [ ] Week 4: Advanced K8s security (NetworkPolicies, RBAC)
- [ ] Week 5+: Monitoring and observability

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Kubernetes (Minikube for local development)
- kubectl
- AWS CLI (for EKS deployment)
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Running Services Individually with Docker

**API Service:**

```bash
cd apps/api-service
docker build -t api-service .
docker run -p 3000:3000 api-service
```

**Auth Service:**

```bash
cd apps/auth-service
docker build -t auth-service .
docker run -p 3001:3001 auth-service
```

**Worker Service:**

```bash
cd apps/worker-service
docker build -t worker-service .
docker run -p 3002:3002 worker-service
```

### Running on Kubernetes (Local)

**Prerequisites:**

- Minikube installed and running (`minikube start`)
- kubectl installed

**Quick Start:**

```bash
# Build images for Minikube
eval $(minikube docker-env)

# Build all service images
cd apps/api-service && docker build -t api-service:v1 . && cd ../..
cd apps/auth-service && docker build -t auth-service:v1 . && cd ../..
cd apps/worker-service && docker build -t worker-service:v1 . && cd ../..

eval $(minikube docker-env -u)

# Deploy all services to Kubernetes
kubectl apply -f k8s/api-service/
kubectl apply -f k8s/auth-service/
kubectl apply -f k8s/worker-service/

# Verify all pods are running
kubectl get pods
```

**Access services:**

```bash
# API Service (keep terminal open)
minikube service api-service --url

# Auth Service (in new terminal)
minikube service auth-service --url

# Worker Service (in new terminal)
minikube service worker-service --url
```

For detailed local Kubernetes usage, see [Kubernetes Guide](k8s/README.md).

### Deploying to AWS EKS

**Prerequisites:**

- AWS EKS cluster provisioned
- `kubectl` configured for your EKS cluster
- AWS ECR repository access
- Docker buildx for multi-platform builds

**Build for EKS (AMD64 architecture):**

```bash
# Setup multi-platform builder (one-time)
docker buildx create --name multiplatform --driver docker-container --use
docker buildx inspect --bootstrap

# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 023231074087.dkr.ecr.us-east-1.amazonaws.com

# Build and push all services
cd apps/api-service
docker buildx build --platform linux/amd64 \
  -t 023231074087.dkr.ecr.us-east-1.amazonaws.com/secure-cloud-platform/api-service:v1 \
  --push .

cd ../auth-service
docker buildx build --platform linux/amd64 \
  -t 023231074087.dkr.ecr.us-east-1.amazonaws.com/secure-cloud-platform/auth-service:v1 \
  --push .

cd ../worker-service
docker buildx build --platform linux/amd64 \
  -t 023231074087.dkr.ecr.us-east-1.amazonaws.com/secure-cloud-platform/worker-service:v1 \
  --push .
```

**Deploy to EKS:**

```bash
# Connect to EKS cluster
aws eks update-kubeconfig --name your-cluster-name --region us-east-1

# Deploy all services
kubectl apply -f k8s-eks/api-service/
kubectl apply -f k8s-eks/auth-service/
kubectl apply -f k8s-eks/worker-service/

# Verify deployment
kubectl get pods
kubectl get services

# Get API LoadBalancer URL
kubectl get service api-service
```

For detailed EKS deployment instructions, troubleshooting, and architecture details, see [EKS Deployment Guide](k8s-eks/README.md).

### Service-to-Service Communication in Kubernetes

Services communicate internally using Kubernetes DNS. Each service can reach others by name:

```bash
# From any pod in the cluster:
curl http://api-service:3000/health
curl http://auth-service:3001/health
curl http://worker-service:3002/health
```

**Testing communication:**

```bash
# Run a test pod with curl
kubectl run curl-test --image=curlimages/curl -it --rm -- sh

# Inside the pod, test services
curl http://auth-service:3001/health
curl http://worker-service:3002/health

# Test auth flow
curl -X POST http://auth-service:3001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Exit (pod auto-deletes)
exit
```

**How it works:**

- Kubernetes DNS automatically resolves service names to pod IPs
- Services load-balance across multiple pod replicas
- Pods can restart/move - DNS continues to work
- No hardcoded IP addresses needed

### Testing the Services

**API Service:**

```bash
curl http://localhost:3000/health
curl http://localhost:3000/api/users
```

**Auth Service:**

```bash
curl -X POST http://localhost:3001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

**Worker Service:**

```bash
curl http://localhost:3002/health
curl -X POST http://localhost:3002/jobs \
  -H "Content-Type: application/json" \
  -d '{"type":"email"}'
```

## Blog Series

I'm documenting this journey on [Dev.to](https://dev.to/jeffgrahamcodes):

1. [What is DevOps? A Definition from a Teacher Transitioning to DevSecOps](https://dev.to/jeffgrahamcodes/what-is-devops-a-definition-from-a-teacher-transitioning-to-devsecops-3b6n)
2. [3 Microservices, 3 Days: What I Learned About DevOps Architecture](https://dev.to/jeffgrahamcodes/3-microservices-3-days-what-i-learned-about-devops-architecture-23n0)
3. [From Docker Containers to Kubernetes Pods: Deploying My First Microservices Platform](https://dev.to/jeffgrahamcodes/from-docker-containers-to-kubernetes-pods-deploying-my-first-microservices-platform-30a7)
4. More posts coming as I build...

## Project Structure

```
secure-cloud-platform/
├── apps/
│   ├── api-service/          # Node.js REST API
│   ├── auth-service/         # JWT authentication service
│   └── worker-service/       # Python background worker
├── k8s/                      # Kubernetes manifests (Minikube)
│   ├── api-service/          # API service K8s deployment
│   ├── auth-service/         # Auth service K8s deployment
│   ├── worker-service/       # Worker service K8s deployment
│   └── README.md             # Local K8s documentation
├── k8s-eks/                  # Kubernetes manifests (AWS EKS)
│   ├── api-service/          # API service EKS deployment
│   ├── auth-service/         # Auth service EKS deployment
│   ├── worker-service/       # Worker service EKS deployment
│   └── README.md             # EKS deployment guide
├── terraform/                # Infrastructure as Code (coming soon)
├── .github/workflows/        # CI/CD pipelines (coming soon)
├── docs/                     # Additional documentation
└── README.md                 # This file
```

## Security Considerations

- All services implement security best practices
- Container security scanning (coming soon)
- JWT-based authentication
- Environment-based secrets management
- Multi-platform Docker builds (ARM64 → AMD64)
- Resource limits and health checks on all pods
- Network policies and RBAC (coming soon)
- Regular security audits planned

## Learning Goals

This project demonstrates proficiency in:

- Microservices architecture
- Container orchestration with Kubernetes
- Multi-environment deployments (local and cloud)
- Infrastructure as Code (in progress)
- DevSecOps practices
- Cloud-native development on AWS
- Platform architecture and cross-compilation
- CI/CD automation (coming soon)

## About

Building this as part of my transition from teaching to DevSecOps engineering. Former Air Force officer, software engineer, and Solutions Architect.

**Certifications:**

- AWS Solutions Architect Professional
- AWS Security Specialty
- AWS Developer Associate
- AWS SysOps Administrator

Connect: [LinkedIn](https://www.linkedin.com/in/jeffgrahamcodes/) | [Dev.to](https://dev.to/jeffgrahamcodes) | [GitHub](https://github.com/jeffgrahamcodes)

---

_This is a learning project built in public. Feedback and suggestions welcome!_
