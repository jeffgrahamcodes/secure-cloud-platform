# Kubernetes Manifests for AWS EKS Deployment

This directory contains Kubernetes manifests for deploying the secure-cloud-platform microservices to AWS EKS.

## Architecture Overview

The platform consists of three microservices:

- **api-service** - REST API gateway (Port 3000) - Exposed via LoadBalancer
- **auth-service** - JWT authentication service (Port 3001) - Internal ClusterIP
- **worker-service** - Background job processor (Port 3002) - Internal ClusterIP

All services run with 2 replicas for high availability.

## Prerequisites

- AWS EKS cluster provisioned and running
- `kubectl` configured to connect to your EKS cluster
- Docker images built for `linux/amd64` platform and pushed to ECR
- AWS ECR repository: `023231074087.dkr.ecr.us-east-1.amazonaws.com/secure-cloud-platform/`

## Directory Structure

```
k8s-eks/
├── api-service/
│   ├── deployment.yaml    # API service deployment with 2 replicas
│   └── service.yaml       # LoadBalancer service for external access
├── auth-service/
│   ├── deployment.yaml    # Auth service deployment with 2 replicas
│   └── service.yaml       # ClusterIP service for internal access
├── worker-service/
│   ├── deployment.yaml    # Worker service deployment with 2 replicas
│   └── service.yaml       # ClusterIP service for internal access
└── README.md
```

## Building Docker Images for EKS

**CRITICAL:** EKS nodes run on AMD64 architecture. If building on ARM Macs, you must build for the correct platform.

### Setup Multi-Platform Builder (One-Time)

```bash
docker buildx create --name multiplatform --driver docker-container --use
docker buildx inspect --bootstrap
```

### Build and Push Images

```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 023231074087.dkr.ecr.us-east-1.amazonaws.com

# Build and push api-service
cd apps/api-service
docker buildx build --platform linux/amd64 \
  -t 023231074087.dkr.ecr.us-east-1.amazonaws.com/secure-cloud-platform/api-service:v1 \
  --push .

# Build and push auth-service
cd ../auth-service
docker buildx build --platform linux/amd64 \
  -t 023231074087.dkr.ecr.us-east-1.amazonaws.com/secure-cloud-platform/auth-service:v1 \
  --push .

# Build and push worker-service
cd ../worker-service
docker buildx build --platform linux/amd64 \
  -t 023231074087.dkr.ecr.us-east-1.amazonaws.com/secure-cloud-platform/worker-service:v1 \
  --push .
```

### Verify Platform Architecture

```bash
docker buildx imagetools inspect 023231074087.dkr.ecr.us-east-1.amazonaws.com/secure-cloud-platform/api-service:v1
```

Look for `Platform: linux/amd64` in the output.

## Deployment

### Connect to EKS Cluster

```bash
aws eks update-kubeconfig --name your-cluster-name --region us-east-1
kubectl config current-context
```

### Deploy All Services

```bash
# Deploy API Service
kubectl apply -f k8s-eks/api-service/deployment.yaml
kubectl apply -f k8s-eks/api-service/service.yaml

# Deploy Auth Service
kubectl apply -f k8s-eks/auth-service/deployment.yaml
kubectl apply -f k8s-eks/auth-service/service.yaml

# Deploy Worker Service
kubectl apply -f k8s-eks/worker-service/deployment.yaml
kubectl apply -f k8s-eks/worker-service/service.yaml
```

### Verify Deployment

```bash
# Check all resources
kubectl get all

# Check pods are running
kubectl get pods

# Check services
kubectl get services

# Get LoadBalancer URL for API
kubectl get service api-service
```

Wait for the LoadBalancer EXTERNAL-IP to be assigned (may take 2-3 minutes).

### Test the Deployment

```bash
# Get the LoadBalancer URL
export API_URL=$(kubectl get service api-service -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')

# Test health endpoint
curl http://$API_URL/health
```

Expected response:

```json
{
  "status": "healthy",
  "service": "api-service",
  "timestamp": "2025-10-16T23:51:26.385Z"
}
```

## Service Configuration

### Resource Limits

All services use the same resource configuration:

```yaml
resources:
  requests:
    memory: '128Mi'
    cpu: '100m'
  limits:
    memory: '256Mi'
    cpu: '200m'
```

### Health Checks

All services implement health probes:

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 3000
  initialDelaySeconds: 10
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /health
    port: 3000
  initialDelaySeconds: 5
  periodSeconds: 5
```

### Replicas

All services run with 2 replicas for high availability.

## Troubleshooting

### Pods in CrashLoopBackOff

Check pod logs:

```bash
kubectl logs <pod-name>
```

Common issues:

- **"exec format error"** - Image built for wrong platform (ARM vs AMD64)
- **Health check failures** - Service not responding on expected port
- **Image pull errors** - ECR permissions or image doesn't exist

### Platform Architecture Issues

If you see "exec format error", the image was built for the wrong architecture.

Verify image platform:

```bash
docker buildx imagetools inspect <image-url>
```

If needed, use specific SHA digest:

```bash
kubectl set image deployment/api-service api=<image-url>@sha256:<digest>
```

### View Pod Events

```bash
kubectl describe pod <pod-name>
```

Look at the Events section for detailed error information.

### Check Service Endpoints

```bash
kubectl get endpoints
```

Endpoints should show pod IPs. If empty, pods aren't passing readiness checks.

## Updating Deployments

### Update Image Version

```bash
kubectl set image deployment/api-service api=<new-image>:v2
```

### Scale Replicas

```bash
kubectl scale deployment api-service --replicas=3
```

### Restart Deployment

```bash
kubectl rollout restart deployment api-service
```

### View Rollout Status

```bash
kubectl rollout status deployment api-service
```

## Service Communication

Services can communicate internally using Kubernetes DNS:

- `http://api-service:80` → api-service
- `http://auth-service:80` → auth-service
- `http://worker-service:80` → worker-service

The service name resolves to the ClusterIP, which load balances across pod replicas.

## Network Architecture

```
Internet
    ↓
AWS ELB (LoadBalancer)
    ↓
api-service (2 replicas) ← Port 80 → Container Port 3000
    ↓
    → auth-service (2 replicas) - Internal only
    → worker-service (2 replicas) - Internal only
```

## What's Not Included (Yet)

This is a basic deployment. Production-ready additions needed:

- [ ] ConfigMaps for application configuration
- [ ] Secrets for sensitive data (JWT keys, DB credentials)
- [ ] Ingress controller for HTTP routing
- [ ] Network policies for service isolation
- [ ] Horizontal Pod Autoscaling
- [ ] Resource quotas and limit ranges
- [ ] Monitoring and logging
- [ ] TLS/SSL certificates

## Next Steps

1. **Configuration Management** - Move hardcoded values to ConfigMaps
2. **Secrets Management** - Implement proper secret handling
3. **Monitoring** - Add Prometheus and Grafana
4. **Logging** - Implement centralized logging
5. **CI/CD** - Automate deployments with GitHub Actions
6. **Infrastructure as Code** - Manage EKS cluster with Terraform

## Related Documentation

- [API Service README](../apps/api-service/README.md)
- [Auth Service README](../apps/auth-service/README.md)
- [Worker Service README](../apps/worker-service/README.md)
- [Main Project README](../README.md)

## Support

Issues or questions? Open an issue on [GitHub](https://github.com/jeffgrahamcodes/secure-cloud-platform/issues).
