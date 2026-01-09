# Research: Habit Tracker Core Logic & Security

## Decision 1: Better Auth + FastAPI JWT Integration
**Decision**: Use `python-jose` for JWT verification in a FastAPI dependency.
**Rationale**: Better Auth issues signed JWTs. To enforce the constitution's "Strict Data Isolation" principle, the backend must verify these tokens on every request.
**Alternatives Considered**: `PyJWT` (rejected for less built-in support for JWKS), `FastAPI-Auth` (rejected for lack of Better Auth integration).

## Decision 2: Serverless Connection Management
**Decision**: Configure SQLModel with `asyncpg` and use Neon's `-pooler` endpoint with optimized pool settings (`pool_size=3`).
**Rationale**: Serverless environments (Neon/FastAPI) require aggressive connection recycling to stay within limits. Async sessions ensure the UI remains responsive during DB I/O.
**Alternatives Considered**: Sequential `psycopg2` (rejected as non-async), `NullPool` (rejected due to higher latency for frequently used endpoints).

## Decision 3: Streak Calculation Algorithm
**Decision**: Perform a backwards iteration from today in the API layer for current streak; use a single ordered query for longest streak.
**Rationale**: Handling gaps correctly is the primary challenge. Calculating current streak on-the-fly ensures dashboard accuracy.
**Alternatives Considered**: Trigger-based pre-calculation in DB (rejected for complexity with habit deletion/edits).

## Decision 4: Framer Motion for Interaction
**Decision**: Use `AnimatePresence` for habit list management and `layout` props for smooth reordering.
**Rationale**: Satisfies the constitutional mandate for a "Modern Animated UI". Staggered entry (delay index * 0.05) provides a polished feel.
**Alternatives Considered**: CSS Transitions (rejected as less flexible for list reorders).
