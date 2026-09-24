# AI_USAGE.md

## 1. MVP scope
**AI suggested:** adding diagrams, code execution, authentication and gamification would make the product feel more complete.
**Decision:** rejected most of these for the first version. The assignment rewards the practice loop and domain design, so I kept three problems and one submission format.

## 2. Evaluation model
**AI suggested:** use a single LLM prompt asking for a 100-point score.
**Decision:** rejected. A fixed rubric with criterion → score → evidence → concern → suggestion is more explainable and testable.

## 3. Evaluation architecture
**AI suggested:** make the LLM call part of the HTTP submission handler.
**Decision:** rejected as a domain coupling. The prototype isolates evaluation behind a function/port-shaped boundary and exposes evaluation states so a slower evaluator can be introduced later.

## 4. Submission format
**AI suggested:** build a full UML editor because LLD is visual.
**Decision:** rejected for the 2-day scope. Structured text gives enough evidence about responsibilities, relationships, trade-offs and edge cases without spending most of the time on editor mechanics.

## 5. Storage
**AI suggested:** start with multiple services and a queue.
**Decision:** rejected. A monolith with a repository boundary is more appropriate for the assignment. If evaluation becomes slow at larger scale, evaluation execution is the first component worth separating.
