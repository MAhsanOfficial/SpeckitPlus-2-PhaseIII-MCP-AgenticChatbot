# Caching Strategy

## Rules
- Implement caching at multiple layers
- Use Redis or Memcached for distributed caching
- Define cache invalidation strategies
- Monitor cache hit rates

## Analysis
This skill optimizes performance through effective caching. Multi-layer caching (CDN, application, database) reduces latency and load at each tier. Distributed caches like Redis enable cache sharing across pods, improving hit rates and consistency. Cache invalidation strategies (TTL, event-based, write-through) balance freshness with performance. Monitoring hit rates identifies caching effectiveness and guides optimization efforts, though cache complexity can introduce subtle bugs and stale data issues if not managed carefully.
