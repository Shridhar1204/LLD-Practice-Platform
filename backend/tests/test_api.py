from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

VALID = {
    "requirements": "The system parks cars and trucks, issues tickets, calculates fees, and supports new pricing rules.",
    "classes": "ParkingLot, Level, ParkingSpot, Vehicle, Ticket, FeeStrategy, StandardFeeStrategy",
    "relationships": "ParkingLot owns Levels; Level owns Spots; Ticket references Vehicle and Spot; FeeStrategy calculates fees.",
    "design_decisions": "Use a Strategy interface for pricing so fee rules can change without modifying the parking lot. Keep vehicle behaviour on Vehicle.",
    "edge_cases": "Full lot, unsupported vehicle/spot combination, duplicate ticket, unparking unknown vehicle, invalid payment, and zero available spots."
}

def test_health():
    assert client.get('/api/health').json()['status'] == 'ok'

def test_create_and_submit_attempt():
    attempt = client.post('/api/attempts', json={'problem_id':'parking-lot'}).json()
    result = client.post(f"/api/attempts/{attempt['id']}/submit", json=VALID)
    assert result.status_code == 200
    body = result.json()
    assert body['status'] == 'Completed'
    assert body['evaluation']['overall_score'] >= 1
    assert len(body['evaluation']['criteria']) == 5

def test_invalid_problem():
    assert client.post('/api/attempts', json={'problem_id':'nope'}).status_code == 404
