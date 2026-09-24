from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Literal
from uuid import uuid4
from datetime import datetime, timezone

app = FastAPI(title="LLD Practice API", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

PROBLEMS = [
    {
        "id": "parking-lot", "title": "Parking Lot", "difficulty": "Medium", "time": "30–45 min",
        "tags": ["OOP", "Strategy", "Factory"],
        "description": "Design a multi-level parking lot that assigns vehicles to suitable spots and calculates parking fees.",
        "requirements": [
            "Support motorcycles, cars and trucks.", "Support multiple parking spot types.",
            "Park and unpark a vehicle with a ticket.", "Calculate fees using a pluggable pricing policy.",
            "Make it easy to add a new vehicle or pricing rule."
        ],
        "evaluation_focus": ["responsibilities", "encapsulation", "strategy", "extensibility", "edge-cases"]
    },
    {
        "id": "vending-machine", "title": "Vending Machine", "difficulty": "Easy", "time": "20–30 min",
        "tags": ["State", "Encapsulation", "Validation"],
        "description": "Design a vending machine that sells products, accepts money, returns change and handles invalid operations.",
        "requirements": [
            "Display products and inventory.", "Accept coins/notes and track inserted money.",
            "Allow product selection and dispense only when payment is sufficient.", "Return change and support cancellation.",
            "Handle sold-out and invalid-selection cases cleanly."
        ],
        "evaluation_focus": ["state", "invariants", "responsibilities", "error-handling", "testability"]
    },
    {
        "id": "elevator", "title": "Elevator System", "difficulty": "Hard", "time": "45–60 min",
        "tags": ["State", "Strategy", "Scheduling"],
        "description": "Design an elevator controller that accepts floor requests and dispatches elevators using a configurable strategy.",
        "requirements": [
            "Support multiple elevators and floors.", "Accept hall and cabin requests.",
            "Track elevator direction and state.", "Choose an elevator using a replaceable dispatch strategy.",
            "Handle door, movement and overload states."
        ],
        "evaluation_focus": ["state", "strategy", "cohesion", "extensibility", "edge-cases"]
    },
]

attempts = {}

class Submission(BaseModel):
    requirements: str = Field(min_length=20)
    classes: str = Field(min_length=20)
    relationships: str = Field(min_length=10)
    design_decisions: str = Field(min_length=20)
    edge_cases: str = Field(min_length=10)

class AttemptCreate(BaseModel):
    problem_id: str

class EvaluationCriterion(BaseModel):
    criterion: str
    score: int
    evidence: str
    concern: str
    suggestion: str
    confidence: Literal["high", "medium", "low"]

class Evaluation(BaseModel):
    overall_score: int
    summary: str
    criteria: list[EvaluationCriterion]
    next_try: list[str]

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.get("/api/problems")
def list_problems():
    return PROBLEMS

@app.get("/api/problems/{problem_id}")
def get_problem(problem_id: str):
    problem = next((p for p in PROBLEMS if p["id"] == problem_id), None)
    if not problem:
        raise HTTPException(404, "Problem not found")
    return problem

@app.post("/api/attempts")
def create_attempt(payload: AttemptCreate):
    if not any(p["id"] == payload.problem_id for p in PROBLEMS):
        raise HTTPException(404, "Problem not found")
    attempt_id = str(uuid4())
    attempts[attempt_id] = {
        "id": attempt_id, "problem_id": payload.problem_id, "status": "Draft",
        "created_at": datetime.now(timezone.utc).isoformat(), "submission": None, "evaluation": None
    }
    return attempts[attempt_id]

@app.get("/api/attempts")
def list_attempts():
    return sorted(attempts.values(), key=lambda x: x["created_at"], reverse=True)

@app.get("/api/attempts/{attempt_id}")
def get_attempt(attempt_id: str):
    if attempt_id not in attempts:
        raise HTTPException(404, "Attempt not found")
    return attempts[attempt_id]


def evaluate(sub: Submission, problem: dict) -> Evaluation:
    text = " ".join([sub.requirements, sub.classes, sub.relationships, sub.design_decisions, sub.edge_cases]).lower()
    classes = [x.strip() for x in sub.classes.replace("\n", ",").split(",") if x.strip()]
    criteria = []
    def add(c, score, evidence, concern, suggestion, conf="high"):
        criteria.append(EvaluationCriterion(criterion=c, score=score, evidence=evidence, concern=concern, suggestion=suggestion, confidence=conf))
    add("Requirement understanding", 4 if len(sub.requirements) > 80 else 3,
        "The submission explicitly states functional requirements and assumptions.",
        "Some requirements are described without observable acceptance behaviour." if len(sub.requirements) <= 80 else "",
        "Turn each important requirement into a concrete behaviour or invariant.")
    responsibility_score = 5 if len(classes) >= 5 else 3
    add("Class responsibilities", responsibility_score,
        f"The design identifies {len(classes)} candidate classes/components.",
        "A small class list can hide overloaded responsibilities." if responsibility_score < 5 else "",
        "Give each class one reason to change and move orchestration into a domain service when needed.")
    has_interface = any(k in text for k in ["interface", "abstract", "protocol"])
    add("Encapsulation & interfaces", 5 if has_interface else 3,
        "The submission discusses an abstraction boundary." if has_interface else "No explicit interface/abstraction was identified.",
        "Concrete dependencies may make future variation harder." if not has_interface else "",
        "Introduce interfaces only around behaviour that is likely to vary; avoid abstractions without a second implementation.")
    pattern = any(k in text for k in ["strategy", "factory", "state", "observer"])
    add("Extensibility", 5 if pattern else 3,
        "A replaceable design mechanism is mentioned." if pattern else "No explicit extension point is described.",
        "The design may require edits to existing classes when a new rule is added." if not pattern else "",
        "Name the change point and show how a new rule/type can be added without changing stable code.")
    edge = 5 if len(sub.edge_cases) > 60 else 3
    add("Edge cases & testability", edge,
        "The submission includes failure/edge-case thinking.",
        "Important failure paths are not yet concrete." if edge < 5 else "",
        "Add tests for invalid state transitions, duplicate requests, empty inventory and boundary values.")
    overall = round(sum(c.score for c in criteria) / len(criteria))
    return Evaluation(overall_score=overall,
        summary="Your design has a workable object model. The biggest opportunity is to make responsibilities and variation points explicit so the design is easier to extend and test.",
        criteria=criteria,
        next_try=["Rewrite one overloaded class into smaller responsibilities.", "Name one interface that isolates a real variation point.", "Add two failure-path tests before changing the design further."])

@app.post("/api/attempts/{attempt_id}/submit")
def submit_attempt(attempt_id: str, submission: Submission):
    if attempt_id not in attempts:
        raise HTTPException(404, "Attempt not found")
    attempt = attempts[attempt_id]
    if attempt["status"] in {"Evaluating", "Completed"}:
        return attempt
    problem = next(p for p in PROBLEMS if p["id"] == attempt["problem_id"])
    attempt["submission"] = submission.model_dump()
    attempt["status"] = "Evaluating"
    # MVP: synchronous evaluator; domain API still exposes an explicit evaluation state.
    try:
        attempt["evaluation"] = evaluate(submission, problem).model_dump()
        attempt["status"] = "Completed"
    except Exception:
        attempt["status"] = "Failed"
        raise HTTPException(500, "Evaluation failed; submission was retained")
    return attempt
