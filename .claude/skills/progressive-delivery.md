# Progressive Delivery

## Rules
- Implement canary deployments for risk mitigation
- Use feature flags for gradual rollouts
- Monitor metrics during rollout
- Define rollback criteria upfront

## Analysis
This skill enables safe, gradual feature releases through progressive delivery techniques. Canary deployments route a small percentage of traffic to new versions, limiting blast radius if issues occur. Feature flags decouple deployment from release, allowing features to be enabled for specific users or gradually rolled out. Monitoring metrics during rollout (error rates, latency, business KPIs) provides early warning of problems. Pre-defined rollback criteria enable automated or quick manual rollback decisions, reducing mean time to recovery during incidents.
