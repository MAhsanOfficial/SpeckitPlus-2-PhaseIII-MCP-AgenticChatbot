# CI/CD for Kubernetes

## Rules
- Automate image building and tagging
- Run security scans in pipeline
- Deploy to staging before production
- Implement automated rollback on failure

## Analysis
This skill establishes automated deployment pipelines for Kubernetes applications. Automated image building ensures consistent builds with proper versioning through Git commit SHAs or semantic versions. Security scanning in the pipeline catches vulnerabilities before deployment, shifting security left. Staging deployments provide a production-like environment for final validation, catching integration issues before they affect users. Automated rollback on failure detection (via health checks or metrics) minimizes downtime and reduces manual intervention during incidents.
