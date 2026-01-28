# Rate Limiting and Throttling

## Rules
- Implement rate limiting at ingress level
- Use token bucket or leaky bucket algorithms
- Provide clear rate limit feedback to clients
- Monitor rate limit hit rates

## Analysis
This skill protects services from abuse and overload through rate limiting. Ingress-level rate limiting provides a first line of defense before requests reach application pods. Token bucket and leaky bucket algorithms provide flexible rate limiting with burst handling capabilities. Clear feedback (429 status codes, Retry-After headers) helps clients implement proper backoff strategies. Monitoring rate limit hits identifies potential abuse or legitimate traffic spikes requiring capacity increases, though overly aggressive rate limiting can degrade user experience.
