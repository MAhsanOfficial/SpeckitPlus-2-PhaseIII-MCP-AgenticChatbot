# Batch Processing Patterns

## Rules
- Use Jobs for one-time tasks
- Use CronJobs for scheduled tasks
- Set appropriate backoffLimit and activeDeadlineSeconds
- Clean up completed jobs automatically

## Analysis
This skill establishes patterns for batch processing in Kubernetes. Jobs ensure tasks run to completion, handling failures through retries and providing completion guarantees. CronJobs schedule recurring tasks like backups, reports, or cleanup operations using familiar cron syntax. BackoffLimit controls retry attempts for failed jobs, while activeDeadlineSeconds prevents runaway jobs from consuming resources indefinitely. Automatic cleanup of completed jobs (via TTL controller or manual policies) prevents cluster clutter, though recent job history should be retained for debugging.
