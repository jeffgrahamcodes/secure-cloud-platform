# Secure Cloud Platform

Three containerized microservices taken from `docker run` on a laptop to a multi-AZ EKS cluster on AWS, with the network and cluster provisioned in Terraform.

The services themselves are small on purpose. The point of this repo is the path: Docker, then Kubernetes on Minikube, then Terraform for a production-shaped VPC and EKS cluster, then the same services running there behind a load balancer.

## Architecture

```
                    Internet
                       │
              ┌──────────▼──────────┐
              │  AWS load balancer  │   (LoadBalancer Service)
              └──────────┬──────────┘
   ┌─────────────────────┼────────────── VPC 10.0.0.0/16 ─────────┐
   │  public subnets     │   us-east-1a / 1b    IGW + NAT gateway │
   │ ────────────────────┼──────────────────────────────────────  │
   │  private subnets    ▼                                        │
   │   ┌──────────────────────── EKS ──────────────────────────┐  │
   │   │  api-service ×2      (:3000, public via LB)           │  │
   │   │  auth-service ×2     (:3001, ClusterIP, internal)     │  │
   │   │  worker-service ×2   (:3002, ClusterIP, internal)     │  │
   │   └───────────────────────────────────────────────────────┘  │
   └──────────────────────────────────────────────────────────────┘
```

| Service | Stack | What it does |
| --- | --- | --- |
| `api-service` | Node.js / Express | Public entry point. Health check and a demo users endpoint |
| `auth-service` | Node.js / Express / jsonwebtoken | Issues, verifies and refreshes JWTs (24h expiry) |
| `worker-service` | Python / Flask | Background job queue with job types, status tracking and a worker thread |

Each service has its own Dockerfile with a container health check, and every Kubernetes deployment runs 2 replicas with CPU/memory requests and limits plus liveness and readiness probes.

## Infrastructure (Terraform)

- [`terraform/vpc`](terraform/vpc): VPC across two AZs, public and private subnets, internet gateway, NAT gateway, route tables, all tagged
- [`terraform/eks`](terraform/eks): EKS cluster in the private subnets, managed node group, separate IAM roles for the control plane and nodes with only the AWS-managed policies they need (cluster, worker node, CNI, ECR read-only)
- [`terraform/learning`](terraform/learning): the first module, an encrypted and versioned S3 bucket

Two stacks instead of one so the VPC can outlive the cluster. The EKS stack finds the VPC by tag.

## Run it

**One service, locally**

```bash
cd apps/auth-service
docker build -t auth-service .
docker run -p 3001:3001 auth-service
curl -X POST localhost:3001/auth/login -H 'Content-Type: application/json' \
  -d '{"username":"admin","password":"admin123"}'
```

**All three on Minikube:** see [`k8s/README.md`](k8s/README.md)

**On EKS**

```bash
cd terraform/vpc && terraform init && terraform apply
cd ../eks       && terraform init && terraform apply
aws eks update-kubeconfig --name secure-cloud-platform-cluster --region us-east-1
```

Then build images for `linux/amd64`, push to ECR, and `kubectl apply -f k8s-eks/`. Full steps, including the ARM Mac gotcha, are in [`k8s-eks/README.md`](k8s-eks/README.md).

**Cost warning:** the NAT gateway and EKS control plane bill by the hour (roughly $35/month and $73/month). `terraform destroy` both stacks when you're done.

## Roadmap

- [x] Three services, Dockerized
- [x] Deployed to Kubernetes locally, service-to-service calls working
- [x] VPC and EKS in Terraform
- [x] Running on EKS behind a load balancer
- [ ] CI/CD in GitHub Actions with Trivy image scanning and Checkov on the Terraform
- [ ] NetworkPolicies so only `api-service` can reach `auth-service` and `worker-service`
- [ ] Secrets out of env defaults and into AWS Secrets Manager via the CSI driver
- [ ] Prometheus and Grafana

## Honest notes

This is a learning build, and a few things are deliberately simple: the auth service uses an in-memory user list with plaintext demo passwords, the JWT secret falls back to a default if unset, and the worker queue lives in process memory. Those are the next things I'd change before anyone relied on it.

## Tech

Terraform · AWS (VPC, EKS, ECR, IAM, S3) · Kubernetes · Docker · Node.js · Express · Python · Flask · JWT
