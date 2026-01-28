# Minikube Best Practices

## Rules
- Use appropriate resource allocation for local cluster
- Enable necessary addons (ingress, metrics-server)
- Use minikube tunnel for LoadBalancer services
- Clean up unused resources regularly

## Analysis
This skill ensures effective local Kubernetes development with Minikube. Appropriate resource allocation (CPU, memory) balances performance with host system availability, typically 2-4 CPUs and 4-8GB RAM. Enabling addons provides production-like features locally, with ingress enabling HTTP routing and metrics-server supporting HPA testing. Minikube tunnel exposes LoadBalancer services on localhost, enabling local testing of ingress controllers. Regular cleanup prevents disk space exhaustion from accumulated images and volumes, though Minikube's single-node nature means some production scenarios (multi-zone deployments, node failures) cannot be fully tested locally.
