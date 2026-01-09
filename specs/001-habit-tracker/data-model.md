# Data Model: Habit Tracker Core

## Entities

### User (Mirroring Better Auth)
- `id`: UUID (Primary Key)
- `email`: String (Unique)
- `hashed_password`: String

### Habit
- `id`: UUID (Primary Key)
- `user_id`: UUID (Foreign Key -> User.id, Index)
- `name`: String (Max 100 chars, Required)
- `description`: String (Nullable)
- `created_at`: DateTime (Default: now())

### Completion
- `id`: UUID (Primary Key)
- `habit_id`: UUID (Foreign Key -> Habit.id, Index)
- `date`: Date (ISO 8601, Index)
- `status`: Boolean (Default: True)
- `created_at`: DateTime (Default: now())

## Relationships
- A **User** has many **Habits**.
- A **Habit** has many **Completions**.
- (Virtual) A **Habit** has one **Streak** (calculated via service logic).

## Validation Rules
- **V-001**: `user_id` must be present on every Habit and Completion.
- **V-002**: Habit `name` cannot be empty.
- **V-003**: Only one Completion per Habit per Date is permitted (Unique constraint on `habit_id` + `date`).

## State Transitions
- **Mark Complete**: Create a `Completion` record for current date.
- **Unmark Complete**: Delete the `Completion` record for the specified date.
