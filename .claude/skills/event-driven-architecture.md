# Event-Driven Architecture

## Rules
- Use message queues for async communication
- Implement idempotent event handlers
- Define event schemas and versioning
- Monitor queue depths and processing lag

## Analysis
This skill enables scalable, decoupled systems through event-driven patterns. Message queues (Kafka, RabbitMQ, NATS) decouple producers from consumers, enabling independent scaling and failure isolation. Idempotent handlers safely process duplicate events, essential for at-least-once delivery guarantees. Event schema versioning allows producers and consumers to evolve independently. Monitoring queue depths and lag identifies processing bottlenecks and capacity issues, though event-driven systems introduce eventual consistency and debugging complexity.
