# Port Management

## Rules
- Use standard ports where possible (80, 443, 5432)
- Document all exposed ports
- Use targetPort to decouple service and container ports
- Avoid port conflicts in local development

## Analysis
This skill ensures proper port configuration in containerized applications. Standard ports improve discoverability and follow conventions (80 for HTTP, 443 for HTTPS, 5432 for PostgreSQL). Documentation helps operators understand service communication patterns. TargetPort in Kubernetes services allows external port (service port) to differ from container port, enabling flexibility without changing application code. Avoiding port conflicts in local development (especially with Minikube) prevents binding errors and enables running multiple services simultaneously. Port management is a basic but critical aspect of service networking.
