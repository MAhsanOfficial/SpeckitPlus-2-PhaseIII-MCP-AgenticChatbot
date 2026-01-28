# Fail Fast Principle

## Rules
- Validate configuration at startup
- Fail immediately on missing dependencies
- Use strict error handling
- Avoid silent failures

## Analysis
This skill promotes early failure detection for faster debugging. Startup validation checks required configuration, dependencies, and permissions before accepting traffic, preventing runtime surprises. Immediate failure on missing dependencies (database unreachable, required service unavailable) provides clear error messages rather than degraded behavior. Strict error handling (no swallowed exceptions) ensures problems are visible. Avoiding silent failures prevents subtle bugs that are difficult to diagnose. Failing fast reduces mean time to detection and resolution, though it requires robust health checks and monitoring to distinguish between transient and permanent failures.
