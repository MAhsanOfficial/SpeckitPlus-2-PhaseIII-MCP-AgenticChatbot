# Ingress and Routing

## Rules
- Use Ingress controllers for HTTP(S) routing
- Implement TLS termination at ingress
- Define path-based and host-based routing
- Configure rate limiting and CORS policies

## Analysis
This skill establishes proper external access patterns for Kubernetes services. Ingress controllers provide a single entry point for HTTP(S) traffic, reducing the need for multiple LoadBalancer services and associated costs. TLS termination at the ingress layer centralizes certificate management and offloads encryption overhead from application pods. Path-based and host-based routing enables multiple services to share a single IP address and domain, simplifying DNS management. Rate limiting protects services from abuse, while CORS policies enable secure cross-origin requests for modern web applications.
