Certainly! Below is the updated `runbook.md` file that focuses on administering and maintaining the "Hello, World!" web server with **Prometheus metrics and alerting**, but **without SSL or HTTPS security**. This runbook covers scaling, logging, monitoring, alerting, and troubleshooting.

---

# Runbook: "Hello, World!" Web Server

This runbook provides guidance for administering and maintaining the "Hello, World!" web server deployed on Kubernetes using Helm, Traefik (on port `80`), and Minikube. It includes **Prometheus metrics and alerting** for monitoring and troubleshooting.

---

## Table of Contents
1. [Application Overview](#application-overview)
2. [Prerequisites](#prerequisites)
3. [Scaling the Application](#scaling-the-application)
4. [Logging](#logging)
5. [Monitoring with Prometheus](#monitoring-with-prometheus)
6. [Alerting with Alertmanager](#alerting-with-alertmanager)
7. [Troubleshooting](#troubleshooting)
8. [Common Tasks](#common-tasks)
   - [Restarting the Application](#restarting-the-application)
   - [Updating the Application](#updating-the-application)
   - [Accessing the Application](#accessing-the-application)
9. [Backup and Recovery](#backup-and-recovery)

---

## Application Overview
The "Hello, World!" web server is a simple FastAPI application that returns `{"message": "Hello, World!"}` when accessed at the root path (`/`). It is deployed on a Kubernetes cluster using Helm, with Traefik as the Ingress controller.

- **Application Image**: `hello-world-fastapi:latest`
- **Service Port**: `8000`
- **Ingress Host**: `hello-world.local`
- **Helm Chart**: `hello-world-chart`
- **Traefik Port**: `80` (default)
- **Prometheus Metrics**: Exposed via `/metrics` endpoint.

---

## Prerequisites
Before performing any operational tasks, ensure the following tools are installed and configured:
- `kubectl`
- `helm`
- `minikube`
- `docker`

Verify that the application is running:
```bash
kubectl get pods
kubectl get svc
kubectl get ingress
```

---

## Scaling the Application
To scale the application horizontally (increase or decrease the number of replicas), update the `replicaCount` value in the `values.yaml` file and upgrade the Helm release.

1. Edit `values.yaml`:
   ```yaml
   replicaCount: 3
   ```

2. Upgrade the Helm release:
   ```bash
   helm upgrade hello-world .
   ```

3. Verify the scaling:
   ```bash
   kubectl get pods
   ```

---

## Logging
Application logs can be accessed using `kubectl logs`.

1. View logs for a specific pod:
   ```bash
   kubectl logs <pod-name>
   ```

2. Stream logs in real-time:
   ```bash
   kubectl logs -f <pod-name>
   ```

3. View logs for all pods in the deployment:
   ```bash
   kubectl logs -l app=<app-label>
   ```

---

## Monitoring with Prometheus
Prometheus is used to monitor the application and cluster. Metrics are exposed by the FastAPI application via the `/metrics` endpoint.

1. Access the Prometheus UI:
   ```bash
   kubectl port-forward svc/prometheus-operated 9090:9090 -n monitoring
   ```
   Open `http://localhost:9090` in your browser.

2. Query metrics:
   - Request latency: `histogram_quantile(0.99, rate(http_request_duration_seconds_bucket{app="hello-world"}[5m]))`
   - Error rate: `rate(http_requests_total{app="hello-world", status=~"5.."}[5m])`
   - CPU usage: `rate(container_cpu_usage_seconds_total{container="hello-world"}[5m])`
   - Memory usage: `container_memory_usage_bytes{container="hello-world"}`

---

## Alerting with Alertmanager
Alertmanager is used to send alerts based on Prometheus metrics. Alerts are configured for the **Four Golden Signals**:
- **Latency**: Request duration.
- **Traffic**: Request rate.
- **Errors**: Error rate.
- **Saturation**: Resource usage.

1. Access the Alertmanager UI:
   ```bash
   kubectl port-forward svc/prometheus-kube-prometheus-alertmanager 9093:9093 -n monitoring
   ```
   Open `http://localhost:9093` in your browser.

2. View and silence alerts as needed.

---

## Troubleshooting
### Application Not Responding
1. Check pod status:
   ```bash
   kubectl get pods
   ```

2. Check pod logs:
   ```bash
   kubectl logs <pod-name>
   ```

3. Verify service and ingress:
   ```bash
   kubectl get svc
   kubectl get ingress
   ```

4. Test the application directly using port-forward:
   ```bash
   kubectl port-forward <pod-name> 8080:8000
   ```
   Access `http://localhost:8080/`.

### Ingress Not Working
1. Check Traefik logs:
   ```bash
   kubectl logs <traefik-pod-name>
   ```

2. Verify Ingress configuration:
   ```bash
   kubectl describe ingress <ingress-name>
   ```

3. Ensure `minikube tunnel` is running:
   ```bash
   minikube tunnel
   ```

---

## Common Tasks

### Restarting the Application
To restart the application, delete the pod. Kubernetes will automatically recreate it.
```bash
kubectl delete pod <pod-name>
```

### Updating the Application
1. Update the Docker image:
   ```bash
   docker build -t hello-world-fastapi .
   minikube image load hello-world-fastapi:latest
   ```

2. Upgrade the Helm release:
   ```bash
   helm upgrade hello-world .
   ```

### Accessing the Application
1. Use port-forward for direct access:
   ```bash
   kubectl port-forward <pod-name> 8080:8000
   ```
   Access `http://localhost:8080/`.

2. Access via Ingress:
   Run `minikube tunnel` and navigate to:
   ```
   http://hello-world.local/
   ```
   Ensure `hello-world.local` is mapped to the Minikube IP in your `/etc/hosts` file:
   ```
   <minikube-ip> hello-world.local
   ```

---

## Backup and Recovery
### Backup
1. Export Helm release configuration:
   ```bash
   helm get values hello-world > hello-world-values.yaml
   ```

2. Backup Kubernetes manifests:
   ```bash
   kubectl get all -l app=<app-label> -o yaml > hello-world-backup.yaml
   ```

### Recovery
1. Restore the Helm release:
   ```bash
   helm install hello-world . -f hello-world-values.yaml
   ```

2. Apply the backup manifests:
   ```bash
   kubectl apply -f hello-world-backup.yaml
   ```

---

## Prometheus Installation
Prometheus is installed using the `kube-prometheus-stack` Helm chart in the `monitoring` namespace.

1. Add the Prometheus Helm repository:
   ```bash
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   helm repo update
   ```

2. Install the `kube-prometheus-stack`:
   ```bash
   helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring
   ```

3. Verify the installation:
   ```bash
   kubectl get pods -n monitoring
   kubectl get svc -n monitoring
   ```

---

## Conclusion
This runbook provides a comprehensive guide for administering and maintaining the "Hello, World!" web server with **Prometheus metrics and alerting**. For further enhancements, consider integrating Grafana for advanced visualization and dashboards.

---

Let me know if you need additional details or enhancements to this runbook!