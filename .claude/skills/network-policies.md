# Network Policies

## Rules
- Implement default-deny network policies
- Allow only necessary pod-to-pod communication
- Restrict egress to required external services
- Document network topology

## Analysis
This skill enforces network segmentation and zero-trust principles in Kubernetes. Default-deny policies block all traffic by default, requiring explicit allow rules for legitimate communication. Restricting pod-to-pod communication limits lateral movement in case of compromise, containing security incidents. Egress restrictions prevent data exfiltration and limit the impact of compromised containers. Documenting network topology provides visibility into service dependencies and supports security audits, though it requires maintenance as the architecture evolves.
