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

- **API Service** - Node.js REST API
- **Auth Service** - JWT-based authentication
- **Worker Service** - Python background job processing

### Infrastructure

- AWS EKS for Kubernetes orchestration
- Terraform for infrastructure provisioning
- GitHub Actions for CI/CD
- Container security scanning (Trivy)
- Network policies and RBAC

## Tech Stack

- **Languages:** Node.js, Python
- **Infrastructure:** Terraform, AWS (EKS, VPC, RDS)
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
- [ ] Weekend: Deploy all services to Kubernetes
- [ ] Week 2: Terraform EKS infrastructure
- [ ] Week 3: CI/CD pipeline with security scanning
- [ ] Week 4: Advanced K8s security (NetworkPolicies, RBAC)
- [ ] Week 5+: Monitoring and observability

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Kubernetes (Minikube for local development)
- kubectl
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
# Build image for Minikube
eval $(minikube docker-env)
cd apps/api-service
docker build -t api-service:v1 .
cd ../..
eval $(minikube docker-env -u)

# Deploy to Kubernetes
kubectl apply -f k8s/api-service/

# Access the service (keep terminal open)
minikube service api-service --url
```

**Verify deployment:**

```bash
# Check pods are running
kubectl get pods

# Check service
kubectl get services

# View logs
kubectl logs -l app=api-service
```

**Test the service:**

```bash
# Use the URL from 'minikube service api-service --url'
curl http://127.0.0.1:<port>/health
curl http://127.0.0.1:<port>/api/users
```

For detailed Kubernetes usage, see [Kubernetes Guide](k8s/README.md).

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

- [What is DevOps? A Definition from a Teacher Transitioning to DevSecOps](https://dev.to/jeffgrahamcodes/what-is-devops-a-definition-from-a-teacher-transitioning-to-devsecops-3b6n)
- More posts coming as I build...

## Project Structure

```
secure-cloud-platform/
├── apps/
│   ├── api-service/          # Node.js REST API
│   ├── auth-service/         # JWT authentication service
│   └── worker-service/       # Python background worker
├── k8s/                      # Kubernetes manifests
│   ├── api-service/          # API service K8s deployment
│   └── README.md             # K8s documentation
├── terraform/                # Infrastructure as Code (coming soon)
├── .github/workflows/        # CI/CD pipelines (coming soon)
├── docs/                     # Additional documentation
└── README.md                 # This file
```

## Security Considerations

- All services implement security best practices
- Container security scanning integrated
- JWT-based authentication
- Environment-based secrets management
- Network policies and RBAC (coming with Kubernetes)
- Regular security audits planned

## Learning Goals

This project demonstrates proficiency in:

- Microservices architecture
- Container orchestration with Kubernetes
- Infrastructure as Code
- DevSecOps practices
- Cloud-native development
- CI/CD automation

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
