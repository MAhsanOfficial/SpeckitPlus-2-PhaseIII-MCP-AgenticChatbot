# Troubleshooting Discipline

## Rules
- Check pod logs first (kubectl logs)
- Inspect pod events (kubectl describe)
- Verify service endpoints (kubectl get endpoints)
- Use ephemeral debug containers for live debugging

## Analysis
This skill establishes systematic troubleshooting approaches for Kubernetes issues. Pod logs reveal application-level errors and are the first debugging step for most issues. Pod events show scheduling failures, image pull errors, and health check failures. Service endpoints verification confirms that services are routing to healthy pods, catching common misconfiguration issues. Ephemeral debug containers allow attaching debugging tools to running pods without modifying the original container image, enabling live troubleshooting without redeployment.
