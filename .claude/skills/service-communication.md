# Service Communication

## Rules
- Use service discovery via DNS
- Implement retry logic with exponential backoff
- Set appropriate timeouts
- Use circuit breakers for external dependencies

## Analysis
This skill establishes reliable service-to-service communication patterns in distributed systems. Kubernetes DNS-based service discovery eliminates hardcoded endpoints and enables dynamic service location. Retry logic with exponential backoff handles transient failures gracefully without overwhelming failing services. Appropriate timeouts prevent cascading failures and resource exhaustion from hanging requests. Circuit breakers protect the system by failing fast when dependencies are unhealthy, allowing them time to recover while preventing request queuing and resource depletion.
