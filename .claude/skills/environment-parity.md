# Environment Parity

## Rules
- Keep dev, staging, and production as similar as possible
- Use same infrastructure-as-code across environments
- Differ only in scale and data, not architecture
- Test promotion path from dev to production

## Analysis
This skill minimizes environment-specific bugs through consistency. Similar environments reduce "works in staging but not production" issues by ensuring the same code paths execute everywhere. Shared infrastructure-as-code (Terraform, Helm charts) prevents configuration drift and simplifies maintenance. Differing only in scale and data means production has more replicas and real data, but the same services and networking. Testing the promotion path validates that artifacts can move through environments successfully, catching deployment issues early.
