# Project Setup Guide

## Kubernetes Cluster Setup with Minikube

### Start Minikube Cluster
```bash
minikube start
```

### Check Current Kubernetes Context
```bash
kubectl config current-context
```

### Verify Cluster Nodes
```bash
kubectl get nodes
```

## Python Project Setup

### Create Virtual Environment
```bash
python -m venv venv
```

### Activate Virtual Environment
```bash
source venv/bin/activate
```

### Install Project Dependencies
```bash
pip install fastapi uvicorn
```

### Generate Requirements File
```bash
pip freeze > requirements.txt
```

### Install Dependencies from Requirements
```bash
pip install -r requirements.txt
```

### Run Python Server Locally
```bash
uvicorn src.main:app --reload
```

### Access Local Server
Open a web browser and navigate to:
- http://127.0.0.1:8000/

## Project Structure
```
project-root/
│
├── venv/             # Virtual environment
├── src/
│   └── main.py       # Main FastAPI application
├── requirements.txt  # Project dependencies
└── README.md         # This documentation file
```

## Notes
- Ensure Python 3.8+ is installed
- Minikube and kubectl must be pre-installed
- Always activate the virtual environment before working on the project