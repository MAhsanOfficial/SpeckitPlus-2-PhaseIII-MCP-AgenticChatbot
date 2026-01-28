# Service Discovery Patterns

## Rules
- Use Kubernetes DNS for service discovery
- Avoid hardcoded service endpoints
- Implement client-side load balancing where appropriate
- Handle service unavailability gracefully

## Analysis
This skill enables dynamic service location in Kubernetes environments. Kubernetes DNS automatically creates DNS records for services, enabling discovery via service names (e.g., database-service.default.svc.cluster.local). Avoiding hardcoded endpoints allows services to be relocated or scaled without code changes. Client-side load balancing (for gRPC or custom protocols) provides more control than server-side load balancing. Graceful handling of unavailability (retries, circuit breakers, fallbacks) prevents cascading failures when dependencies are down. Service discovery is fundamental to microservices architectures and enables the dynamic nature of Kubernetes deployments.
