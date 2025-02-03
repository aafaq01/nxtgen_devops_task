Certainly! Below is the updated `runbook.md` with Traefik installed using the **default configuration on port 80**. This ensures that Traefik listens on port `80` as expected, and the application is accessed via the standard HTTP port.

---

# Runbook: "Hello, World!" Web Server

This runbook provides guidance for administering and maintaining the "Hello, World!" web server deployed on Kubernetes using Helm, Traefik (on port `80`), and Minikube. It covers common operational tasks such as scaling, logging, monitoring, and troubleshooting.

---

## Table of Contents
1. [Application Overview](#application-overview)
2. [Prerequisites](#prerequisites)
3. [Scaling the Application](#scaling-the-application)
4. [Logging](#logging)
5. [Monitoring](#monitoring)
6. [Troubleshooting](#troubleshooting)
7. [Common Tasks](#common-tasks)
   - [Restarting the Application](#restarting-the-application)
   - [Updating the Application](#updating-the-application)
   - [Accessing the Application](#accessing-the-application)
8. [Backup and Recovery](#backup-and-recovery)

---

## Application Overview
The "Hello, World!" web server is a simple FastAPI application that returns `{"message": "Hello, World!"}` when accessed at the root path (`/`). It is deployed on a Kubernetes cluster using Helm, with Traefik as the Ingress controller.

- **Application Image**: `hello-world-fastapi:latest`
- **Service Port**: `8000`
- **Ingress Host**: `hello-world.local`
- **Helm Chart**: `hello-world-chart`
- **Traefik Port**: `80` (default)

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

## Monitoring
To monitor the application and cluster, consider setting up Prometheus and Grafana. For now, you can use the following commands to monitor resource usage:

1. View pod resource usage:
   ```bash
   kubectl top pods
   ```

2. View node resource usage:
   ```bash
   kubectl top nodes
   ```

3. Check Traefik metrics (if enabled):
   Access the Traefik dashboard:
   ```bash
   kubectl port-forward svc/traefik 9000:9000
   ```
   Open `http://localhost:9000/dashboard/` in your browser.

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

## Traefik Installation (Default on Port 80)
Traefik is installed using Helm with the default configuration, which listens on port `80`. To install Traefik:

1. Add the Traefik Helm repository:
   ```bash
   helm repo add traefik https://helm.traefik.io/traefik
   helm repo update
   ```

2. Install Traefik:
   ```bash
   helm install traefik traefik/traefik
   ```

3. Verify Traefik installation:
   ```bash
   kubectl get pods -l app.kubernetes.io/name=traefik
   kubectl get svc -l app.kubernetes.io/name=traefik
   ```

---

## Conclusion
This runbook provides a comprehensive guide for administering and maintaining the "Hello, World!" web server with Traefik installed on the default port `80`. For further enhancements, consider integrating Prometheus for advanced monitoring and Alertmanager for proactive alerting.

---

Let me know if you need additional details or enhancements to this runbook!