# Blue-Green Deployments

## Rules
- Maintain two identical production environments
- Route traffic via service selector changes
- Validate green environment before cutover
- Keep blue environment for quick rollback

## Analysis
This skill enables zero-downtime deployments with instant rollback capability. Two identical environments (blue=current, green=new) allow thorough validation before traffic cutover. Service selector changes instantly route all traffic to the new version, avoiding gradual rollout complexity. Pre-cutover validation in the green environment catches issues before user impact. Maintaining the blue environment enables instant rollback by reverting the service selector, though running duplicate environments doubles resource costs during deployment windows.
