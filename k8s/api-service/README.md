# Kubernetes Deployment

Kubernetes manifests for deploying the secure-cloud-platform to a Kubernetes cluster.

## Prerequisites

- Kubernetes cluster (Minikube for local development)
- kubectl configured
- Docker images built

## Local Development with Minikube

### Setup

```bash
# Start Minikube
minikube start

# Verify cluster is running
kubectl cluster-info
kubectl get nodes
```

### Build Images for Minikube

Minikube has its own Docker environment. Build images there:

```bash
# Point terminal to Minikube's Docker
eval $(minikube docker-env)

# Build API service image
cd apps/api-service
docker build -t api-service:v1 .

# Return to project root
cd ../..

# Reset Docker environment when done
eval $(minikube docker-env -u)
```

### Deploy API Service

```bash
# Apply manifests
kubectl apply -f k8s/api-service/

# Check deployment status
kubectl get deployments
kubectl get pods
kubectl get services

# Wait for pods to be ready
kubectl get pods -w
# Press Ctrl+C when pods show Running
```

### Access the Service

Minikube requires a tunnel to access NodePort services:

```bash
# Start service tunnel (keep this terminal open)
minikube service api-service --url

# In a new terminal, use the URL provided
curl http://127.0.0.1:<port>/health
curl http://127.0.0.1:<port>/api/users
```

**Alternative: Port Forwarding**

```bash
# Forward pod port to localhost
kubectl port-forward deployment/api-service 3000:3000

# In another terminal
curl http://localhost:3000/health
```

## Kubernetes Manifests Explained

### Deployment (`deployment.yaml`)

Manages pods and ensures desired state:

```yaml
replicas: 2 # Run 2 copies of the service
```

**Key features:**

- **Resource limits** - Memory (128Mi-256Mi) and CPU (100m-200m)
- **Health checks** - Liveness probe (restart if unhealthy) and Readiness probe (route traffic when ready)
- **imagePullPolicy: Never** - Use local image, don't pull from registry

### Service (`service.yaml`)

Exposes pods on a stable network endpoint:

```yaml
type: NodePort # Expose outside cluster
nodePort: 30000 # External port (30000-32767 range)
```

**Service types:**

- **NodePort** - Exposes on each node's IP (development/testing)
- **LoadBalancer** - Cloud provider load balancer (production)
- **ClusterIP** - Internal only (default)

## Useful Commands

### Viewing Resources

```bash
# All resources in namespace
kubectl get all

# Pods
kubectl get pods
kubectl get pods -o wide  # More details (IP, node)

# Deployments
kubectl get deployments

# Services
kubectl get services

# Watch resources update
kubectl get pods -w
```

### Debugging

```bash
# Pod logs
kubectl logs <pod-name>
kubectl logs -f <pod-name>  # Follow logs

# All pods in deployment
kubectl logs -l app=api-service

# Describe resource (shows events, errors)
kubectl describe pod <pod-name>
kubectl describe deployment api-service
kubectl describe service api-service

# Shell into pod
kubectl exec -it <pod-name> -- sh

# Run command in pod
kubectl exec <pod-name> -- curl http://localhost:3000/health
```

### Scaling

```bash
# Scale deployment
kubectl scale deployment api-service --replicas=3

# View replica count
kubectl get deployment api-service

# Auto-healing: delete a pod and watch it recreate
kubectl delete pod <pod-name>
kubectl get pods -w
```

### Updates and Rollbacks

```bash
# Update image
kubectl set image deployment/api-service api=api-service:v2

# Rollout status
kubectl rollout status deployment/api-service

# Rollout history
kubectl rollout history deployment/api-service

# Rollback to previous version
kubectl rollout undo deployment/api-service

# Rollback to specific revision
kubectl rollout undo deployment/api-service --to-revision=1
```

### Cleanup

```bash
# Delete specific service
kubectl delete -f k8s/api-service/

# Delete all resources in namespace
kubectl delete all --all

# Stop Minikube
minikube stop

# Delete Minikube cluster
minikube delete
```

## Project Structure

```
k8s/
├── api-service/
│   ├── deployment.yaml    # Defines pods and replicas
│   └── service.yaml       # Exposes pods on network
├── auth-service/          # Coming soon
├── worker-service/        # Coming soon
└── README.md              # This file
```

## Key Kubernetes Concepts

### Pod

Smallest deployable unit. Contains one or more containers that share network and storage.

### Deployment

Manages pods. Handles:

- Scaling (replicas)
- Rolling updates
- Self-healing (recreates failed pods)
- Rollbacks

### Service

Stable network endpoint for pods. Provides:

- DNS name (e.g., `api-service`)
- Load balancing across pods
- Service discovery

### Label Selector

How Services find Pods:

```yaml
# Service selector
selector:
  app: api-service

# Pod labels (in Deployment template)
labels:
  app: api-service
```

### Health Checks

- **Liveness Probe** - Is the container healthy? If not, restart it.
- **Readiness Probe** - Is the container ready for traffic? If not, remove from Service endpoints.

## Troubleshooting

### Pods not starting

```bash
# Check pod events
kubectl describe pod <pod-name>

# Common issues:
# - Image not found: Build image in Minikube Docker
# - ImagePullBackOff: Check imagePullPolicy
# - CrashLoopBackOff: Check logs for application errors
```

### Can't access service

```bash
# Verify service has endpoints
kubectl describe service api-service

# If no endpoints, check pod labels match service selector
kubectl get pods --show-labels

# For Minikube, use tunnel
minikube service api-service --url
```

### Pods running but not responding

```bash
# Check logs
kubectl logs <pod-name>

# Check if app is listening on correct port
kubectl exec <pod-name> -- netstat -tlnp

# Test from within cluster
kubectl run curl-test --image=curlimages/curl -it --rm -- curl http://api-service:3000/health
```

## Production Considerations

For production Kubernetes deployment:

- **Use LoadBalancer or Ingress** instead of NodePort for external access
- **Implement ConfigMaps** for non-sensitive configuration
- **Use Secrets** for sensitive data (passwords, API keys)
- **Set resource quotas** to prevent resource exhaustion
- **Implement network policies** to restrict pod-to-pod communication
- **Add monitoring** with Prometheus and Grafana
- **Set up logging** with ELK stack or CloudWatch
- **Use namespaces** for environment isolation (dev, staging, prod)
- **Implement RBAC** for security and access control
- **Add horizontal pod autoscaling** based on CPU/memory
- **Use persistent volumes** for stateful workloads
- **Implement service mesh** (Istio, Linkerd) for advanced traffic management

## Next Steps

- [ ] Deploy auth-service to Kubernetes
- [ ] Deploy worker-service to Kubernetes
- [ ] Implement service-to-service communication
- [ ] Add ConfigMaps for configuration
- [ ] Add Secrets for sensitive data
- [ ] Set up Ingress for external access
- [ ] Implement NetworkPolicies for security
- [ ] Add monitoring with Prometheus
- [ ] Create production-ready manifests for EKS

## Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)
- [Kubernetes Patterns](https://k8spatterns.com/)

---

**Part of the [secure-cloud-platform](../README.md) project**
