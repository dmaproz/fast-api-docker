# Python Flask Application - Documentation

## Table of Contents

1. [Overview](#overview)
2. [Application Details](#application-details)
3. [API Endpoints](#api-endpoints)
4. [Docker Setup](#docker-setup)
5. [Kubernetes Deployment](#kubernetes-deployment)
6. [Helm Charts](#helm-charts)
7. [Configuration](#configuration)
8. [Development](#development)

---

## Overview

This project is a Python Flask web application containerized with Docker and configured for deployment on Kubernetes. The application provides basic information endpoints and health checks, designed to run in a containerized environment.

**Project Type:** Web Service  
**Framework:** Flask 3.0.3  
**Python Version:** 3.10  
**Base Image:** python:3.10-alpine3.23  
**Deployment Platform:** Kubernetes

---

## Application Details

### Technology Stack

- **Framework:** Flask 3.0.3
- **Additional Libraries:**
  - Flask-JSON 0.4.0
- **Python Version:** 3.10
- **Container Base:** Alpine Linux 3.23

### Application Structure

```
fast-api-docker/
├── app/
│   └── app.py          # Main Flask application
├── Dockerfile          # Docker image definition
├── requirements.txt    # Python dependencies
├── k8s/                # Kubernetes manifests
├── charts/             # Helm charts
└── docs/               # Documentation
```

### Main Application File

The application is located in `app/app.py` and contains:
- Flask application initialization
- Two main endpoints (info and health check)
- Hostname and timestamp information

---

## API Endpoints

### 1. Information Endpoint

**Endpoint:** `GET /app/v1/info`

**Description:** Returns application information including hostname, current time, and deployment status.

**Response:**
```json
{
  "message": "We are going forward! Some stuffs extra!......",
  "hostname": "<container-hostname>",
  "time": "<current-datetime>",
  "deployed_on": "kubernates"
}
```

**Example:**
```bash
curl http://localhost:5000/app/v1/info
```

### 2. Health Check Endpoint

**Endpoint:** `GET /app/v1/healthz`

**Description:** Health check endpoint for Kubernetes liveness and readiness probes.

**Response:**
```json
{
  "status": "ok"
}
```

**Status Code:** 200

**Example:**
```bash
curl http://localhost:5000/app/v1/healthz
```

---

## Docker Setup

### Dockerfile

The application uses a multi-stage Docker build process:

```dockerfile
FROM python:3.10-alpine3.23
COPY requirements.txt /tmp
RUN pip install --upgrade -r /tmp/requirements.txt
COPY ./app /app
CMD python /app/app.py
```

### Building the Docker Image

```bash
docker build -t python-app:latest .
```

### Running the Container

```bash
docker run -p 5000:5000 python-app:latest
```

The application will be available at `http://localhost:5000`

### Docker Image Details

- **Base Image:** `python:3.10-alpine3.23` (lightweight Alpine Linux)
- **Working Directory:** `/app`
- **Exposed Port:** 5000 (default Flask port)
- **Command:** Runs `app.py` directly

---

## Kubernetes Deployment

### Deployment Manifests

The project includes Kubernetes manifests in the `k8s/` directory:

#### 1. Deployment (`k8s/deploy.yaml`)

- **Name:** `python-app`
- **Replicas:** 1
- **Image:** `dcaroc/fast-api-docker:v2`
- **Container Port:** 5000
- **Labels:** `app: python-app`

#### 2. Service (`k8s/service.yaml`)

- **Name:** `python-app`
- **Type:** ClusterIP (default)
- **Port:** 8080
- **Target Port:** 5000
- **Selector:** `app: python-app`

#### 3. Ingress (`k8s/ingress.yaml`)

- **Name:** `python-app`
- **Host:** `python-app.parcer.com`
- **Path:** `/app/`
- **Path Type:** Prefix
- **Backend Service:** `python-app:8080`

### Deploying to Kubernetes

```bash
# Apply all manifests
kubectl apply -f k8s/deploy.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml

# Check deployment status
kubectl get deployments
kubectl get services
kubectl get ingress
```

### Accessing the Application

After deployment, the application can be accessed via:
- **Internal:** `http://python-app:8080`
- **External:** `http://python-app.parcer.com/app/` (via Ingress)

---

## Helm Charts

### Chart Structure

The Helm chart is located in `charts/python-app/`:

```
charts/python-app/
├── Chart.yaml           # Chart metadata
├── values.yaml          # Default configuration values
└── templates/
    ├── deployment.yaml  # Deployment template
    ├── service.yaml     # Service template
    ├── ingress.yaml     # Ingress template
    └── _helpers.tpl     # Template helpers
```

### Chart Information

- **Chart Name:** `python-app`
- **Chart Version:** 0.1.0
- **App Version:** 1.16.0
- **Type:** Application chart

### Key Configuration Values

From `values.yaml`:

- **Replica Count:** 1
- **Image Repository:** `dcaroc/fast-api-docker`
- **Image Tag:** `7a86a2`
- **Service Type:** ClusterIP
- **Service Port:** 5000
- **Ingress Enabled:** true
- **Ingress Host:** `python-app.parcer.com`
- **Ingress Class:** nginx
- **Resources:**
  - CPU Request: 50m
  - Memory Request: 50M
- **Health Checks:**
  - Liveness Probe: `/app/v1/healthz`
  - Readiness Probe: `/app/v1/healthz`

### Installing with Helm

```bash
# Install the chart
helm install python-app ./charts/python-app

# Install with custom values
helm install python-app ./charts/python-app -f custom-values.yaml

# Upgrade existing installation
helm upgrade python-app ./charts/python-app

# Uninstall
helm uninstall python-app
```

### Customizing Deployment

Create a custom `values.yaml` file to override default values:

```yaml
replicaCount: 3
image:
  repository: your-registry/python-app
  tag: latest
service:
  type: LoadBalancer
  port: 5000
ingress:
  enabled: true
  hosts:
    - host: your-domain.com
      paths:
        - path: /
          pathType: Prefix
resources:
  requests:
    cpu: 100m
    memory: 100M
```

---

## Configuration

### Environment Variables

Currently, the application doesn't require any environment variables. All configuration is hardcoded in the application file.

### Port Configuration

- **Application Port:** 5000 (Flask default)
- **Service Port:** 8080 (Kubernetes service)
- **Container Port:** 5000

### Health Check Configuration

The application implements health checks at `/app/v1/healthz` which are used by Kubernetes for:
- **Liveness Probes:** Determine if the container is running
- **Readiness Probes:** Determine if the container is ready to accept traffic

### Resource Limits

Default resource configuration:
- **CPU Request:** 50m (0.05 cores)
- **Memory Request:** 50M (50 megabytes)

These can be adjusted in the Helm `values.yaml` file or Kubernetes deployment manifests.

---

## Development

### Local Development Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application:**
   ```bash
   python app/app.py
   ```

3. **Test Endpoints:**
   ```bash
   # Test info endpoint
   curl http://localhost:5000/app/v1/info
   
   # Test health endpoint
   curl http://localhost:5000/app/v1/healthz
   ```

### Development Workflow

1. Make changes to `app/app.py`
2. Test locally
3. Build Docker image
4. Test Docker container
5. Deploy to Kubernetes (or use Helm)

### Building and Pushing Docker Image

```bash
# Build image
docker build -t dcaroc/fast-api-docker:latest .

# Tag for specific version
docker tag dcaroc/fast-api-docker:latest dcaroc/fast-api-docker:v2

# Push to registry
docker push dcaroc/fast-api-docker:latest
docker push dcaroc/fast-api-docker:v2
```

### Testing

The application can be tested using:

- **curl:** Command-line HTTP client
- **Postman:** API testing tool
- **Browser:** Direct access to endpoints

### Backstage Integration

The project includes a `catalog-info.yaml` file for Backstage integration:

- **Component Name:** python-app
- **Type:** service
- **Owner:** capes
- **Lifecycle:** experimental
- **GitHub Repository:** dmaproz/fast-api-docker

---

## Additional Notes

### Security Considerations

- The application runs in debug mode (`debug=True`) which should be disabled in production
- Consider implementing authentication/authorization for production use
- Review and update dependencies regularly for security patches

### Scaling

The application can be scaled horizontally by:
- Increasing replica count in Kubernetes deployment
- Enabling autoscaling in Helm values (currently disabled)
- Configuring HPA (Horizontal Pod Autoscaler) based on CPU/memory metrics

### Monitoring

Consider adding:
- Application logging
- Metrics collection (Prometheus)
- Distributed tracing
- Error tracking

### Future Improvements

- Add environment-based configuration
- Implement proper logging
- Add unit and integration tests
- Set up CI/CD pipeline
- Add API documentation (Swagger/OpenAPI)
- Implement graceful shutdown
- Add request rate limiting
- Configure proper security headers

---

## Support

For issues, questions, or contributions, please refer to the GitHub repository: [dmaproz/fast-api-docker](https://github.com/dmaproz/fast-api-docker)

---

**Last Updated:** Generated automatically from project files

