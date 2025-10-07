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
- **Auth Service** - Authentication microservice
- **Worker Service** - Python background processing

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
- [ ] Week 1: Build API service with Docker
- [ ] Week 1-2: Local Kubernetes setup (Minikube/Kind)
- [ ] Week 2: Terraform EKS infrastructure
- [ ] Week 3: CI/CD pipeline with security scanning
- [ ] Week 4: Advanced K8s security (NetworkPolicies, RBAC)
- [ ] Week 5+: Monitoring and observability

## Getting Started

_Coming soon - instructions for running locally_

## Blog Series

I'm documenting this journey on [Dev.to](https://dev.to/jeffgrahamcodes):

- [What is DevOps?](https://dev.to/jeffgrahamcodes/what-is-devops-a-definition-from-a-teacher-transitioning-to-devsecops-3b6n)
- More posts coming as I build...

## About

Building this as part of my transition from teaching to DevSecOps engineering. Former Air Force officer, software engineer, and Solutions Architect.

**Certifications:** AWS Solutions Architect Pro, AWS Security Specialty, AWS Developer Associate, AWS SysOps Administrator

Connect: [LinkedIn](https://www.linkedin.com/in/jeffgrahamcodes/) | [Dev.to](https://dev.to/jeffgrahamcodes)

---

_This is a learning project built in public. Feedback and suggestions welcome!_
