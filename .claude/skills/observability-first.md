# Observability First

## Rules
- Implement health checks (liveness and readiness)
- Structured logging with correlation IDs
- Expose metrics endpoints
- Distributed tracing for multi-service calls

## Analysis
This skill establishes observability as a first-class concern in cloud-native applications. Health checks enable Kubernetes to automatically restart failed containers and route traffic only to ready instances, improving reliability. Structured logging with correlation IDs allows tracing requests across services and aggregating logs effectively. Metrics endpoints enable monitoring systems to collect performance data for alerting and capacity planning. Distributed tracing provides visibility into complex request flows across microservices, essential for debugging and performance optimization in distributed systems.
