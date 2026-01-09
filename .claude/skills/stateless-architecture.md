# Stateless Architecture

## Rules
- Server holds no memory
- All state is persisted in database
- Every request is self-contained

## Analysis
This skill enforces a truly stateless server architecture where no in-memory state exists between requests. All data is persisted to the database, ensuring that any server instance can handle any request at any time. Each request contains all information needed for processing, enabling horizontal scaling, fault tolerance, and simplified load balancing without session affinity requirements.
