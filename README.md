# DesignLoop — LLD Practice Platform

A focused 2-day MVP for practicing Low-Level Design through a repeatable loop:

**Choose problem → Design → Submit → Explainable feedback → Review → Try again**

## Why this product

LLD practice is open-ended: multiple designs can be valid, so a single reference answer or opaque AI score is a poor learning signal. DesignLoop uses a fixed submission structure and rubric so feedback can point to evidence in the learner's own design.

## MVP

- 3 LLD problems: Parking Lot, Vending Machine, Elevator System.
- Structured text submission: requirements, classes/responsibilities, relationships, design decisions, edge cases/tests.
- Explicit attempt lifecycle: Draft → Evaluating → Completed / Failed.
- Explainable rubric feedback across five dimensions.
- Attempt history and review.
- Evaluator isolated behind a domain function so an LLM/rule evaluator can be swapped later.

## Stack

- Frontend: Next.js 15 + React + TypeScript.
- Backend: FastAPI + Python.
- Persistence for the prototype: in-memory repository (keeps the 2-day MVP small). Production follow-up: PostgreSQL repository.
- AI: intentionally abstracted; current evaluator is deterministic. This makes the prototype reliable and testable while leaving a clear seam for an LLM evaluator.

## Run

### Backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000.

## Tests

```bash
cd backend
pytest -q
```

## Design choices

### Why structured text?

A diagram editor or code sandbox gives more evidence but adds implementation risk. The five fields force the learner to expose the exact design decisions the rubric evaluates. A future `SubmissionContent` interface can support diagram/code without changing the practice flow.

### Deterministic vs AI evaluation

Deterministic checks should own submission validity, lifecycle transitions, required structure and known invariants. Judgment-heavy concerns such as cohesion, trade-offs and abstraction quality are good candidates for an LLM. The MVP keeps the evaluator deterministic to make the end-to-end flow reproducible; an LLM adapter can later implement the same `Evaluation` shape.

### Slow/failing evaluation

The submission is stored before evaluation. The API exposes `Evaluating` and `Failed` states. The current prototype evaluates synchronously because the assignment is small; a production version could enqueue evaluation and poll/stream the result without changing the learner-facing state model.

### Extensibility change tests

**Submission changes:** the domain should store a generic submission payload plus a submission type; adding `diagram` should not rewrite `Attempt` or the review flow.

**Evaluator changes:** define an `Evaluator` port with `evaluate(problem, submission) -> Evaluation`; deterministic, LLM and human evaluators can implement it independently.

## Limitations

- No authentication.
- Attempts are in memory and reset when the backend restarts.
- No actual LLM call in the default path.
- No collaborative diagram editor or code execution sandbox.
- Evaluation is intentionally a prototype rubric, not a claim of objective design quality.

See `docs/RESEARCH.md`, `docs/DESIGN.md`, and `AI_USAGE.md`.
