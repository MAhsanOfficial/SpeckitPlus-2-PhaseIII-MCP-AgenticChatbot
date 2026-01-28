# API Gateway Pattern

## Rules
- Centralize cross-cutting concerns at gateway
- Implement authentication and rate limiting
- Route requests to appropriate services
- Provide API versioning and transformation

## Analysis
This skill establishes API gateway patterns for microservices architectures. Centralizing cross-cutting concerns (auth, logging, rate limiting) at the gateway reduces duplication across services. Authentication at the gateway protects backend services and simplifies security implementation. Request routing enables service discovery abstraction and traffic management. API versioning and transformation support client compatibility while allowing backend evolution, though gateways can become bottlenecks and single points of failure requiring careful capacity planning.
