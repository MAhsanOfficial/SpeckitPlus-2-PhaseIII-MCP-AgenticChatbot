# Service Mesh Adoption

## Rules
- Implement service mesh for complex microservices
- Use for traffic management and observability
- Enable mutual TLS between services
- Gradually adopt, starting with non-critical services

## Analysis
This skill guides service mesh adoption for advanced microservices architectures. Service meshes (Istio, Linkerd) provide traffic management, observability, and security without application code changes. Traffic management enables canary deployments, circuit breaking, and retry logic at the infrastructure level. Mutual TLS encrypts service-to-service communication and provides identity verification, enhancing zero-trust security. Gradual adoption reduces risk by starting with non-critical services, allowing teams to learn the technology before applying it broadly, though service meshes add operational complexity and resource overhead.
