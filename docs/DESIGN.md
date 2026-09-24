# Design Note

## User flow

1. Browse a small problem set.
2. Open a problem and inspect requirements.
3. Start an attempt.
4. Submit structured design evidence.
5. Attempt enters `Evaluating`.
6. Evaluator produces a structured `Evaluation`.
7. Learner reviews criterion-level evidence, concerns and suggestions.
8. Attempt remains in history for comparison and retry.

## Domain model

- **Problem** — owns the interview prompt, requirements and evaluation focus.
- **Attempt** — owns the learner's practice lifecycle and references one Problem.
- **Submission** — captures the learner's design evidence. It is deliberately content-oriented rather than tied to a specific editor.
- **Evaluator** — variation point for deterministic, LLM or human evaluation.
- **Evaluation** — immutable-looking result shape containing criterion scores, evidence, concerns, suggestions and confidence.
- **Rubric criterion** — defines what the evaluator is looking for.

## Evaluation

The MVP rubric uses five criteria:

1. Requirement understanding
2. Class responsibilities
3. Encapsulation & interfaces
4. Extensibility
5. Edge cases & testability

Each criterion returns score, evidence, concern, suggestion and confidence. This avoids an unexplained aggregate score.

## Key trade-offs

- **Structured text over diagram/code:** lower implementation cost while preserving enough design signal for an MVP.
- **Synchronous evaluation now:** simpler demo and fewer moving parts. State boundaries make asynchronous evaluation a later implementation detail.
- **In-memory storage:** fastest path for a 2-day prototype. A repository abstraction can later back attempts with PostgreSQL.
- **Deterministic evaluator first:** reliable tests and repeatable demos. LLM evaluation can be added behind the same evaluator contract for qualitative judgement.

## Scale boundary

If usage grows, the first component to separate is evaluation execution, because it can be slow and failure-prone. Submission persistence remains the source of truth; a worker can consume an evaluation job and update the attempt state. There is no need for microservices before that bottleneck exists.
