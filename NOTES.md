# Notes

### Summary of Changes
- **SQL & PL/SQL**: Fixed boolean operator precedence in `TaskRepository`, `search_tasks.sql`, and `task_search_pkg` by wrapping title/description `OR` conditions in parentheses. Prevents archived tasks from leaking and fixes bypassed status filters. Added pagination bounds checking in PL/SQL.
- **Backend**: Removed the artificial `Thread.sleep` latency in `TaskController`. Added safe `TaskStatus` enum validation (returning 400 Bad Request on invalid input instead of 500), and guarded `page`/`pageSize` against non-positive values. Added automated tests.
- **Frontend**: Added `AbortController` cancellation in `useTasks` to eliminate race conditions from out-of-order responses, fixed stuck loading state on errors, and reset pagination `page = 1` on search/filter changes in `App.jsx`.

### What I Chose Not to Change & Why
- **In-Memory Java Pagination**: Kept database fetching all matching rows and slicing in Java rather than rewriting repository queries with Spring Data `Pageable` / SQL `OFFSET`. For the current data scale, avoiding a major repository refactor preserves a focused patch.
- **Debounce Hook / Library**: Kept native state dispatch with `AbortController` cancellation instead of introducing third-party debounce libraries.
- **Component Styling & Layout**: Avoided unnecessary UI redesigns as existing styles satisfy requirements.

### Biggest Remaining Risk
- **Scalability & Database-level Pagination**: As the `tasks` table grows, loading full result sets into Java memory (`subList`) and executing unindexed wildcard `LIKE %term%` queries will cause severe database I/O bottlenecks and JVM heap pressure. Implementing database-level pagination and full-text indexing is critical for production.

### Tools & AI Usage
- Used AI assistant to inspect multi-layer interactions, verify SQL operator precedence semantics, draft the `AbortController` cleanup hook, and construct regression test fixtures.
