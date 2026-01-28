# Graceful Shutdown

## Rules
- Handle SIGTERM signals properly
- Complete in-flight requests before exit
- Set appropriate terminationGracePeriodSeconds
- Deregister from service discovery early

## Analysis
This skill ensures zero-downtime deployments through proper shutdown handling. SIGTERM signal handling allows applications to clean up resources and close connections gracefully. Completing in-flight requests prevents user-facing errors during rolling updates or scaling down. Setting appropriate grace periods (typically 30-60 seconds) gives applications time to finish work before SIGKILL. Early deregistration from service discovery stops new requests from being routed to terminating pods, though the application must continue serving existing requests until completion.
