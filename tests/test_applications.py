from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_applications():
    response = client.get("/applications/1")
    data = response.json()
    application = data["application"]
    assert response.status_code == 200
    assert application["id"] == 1
    assert application["company"] == "Company A"
    assert application["status"] == "Applied"

def test_get_application_not_found():
    response = client.get("/applications/99")
    assert response.status_code == 404
    assert response.json() == {"detail": "Application not found"}

def test_create_application():
    new_application = {
        "company" : "Apple",
        "position" : "Engineer",
        "status" : "Interview"
    }

    response = client.post("/applications", json=new_application)
    data = response.json()
    application = data["application"]
    assert response.status_code == 201
    assert application["company"] == new_application["company"]
    assert application["position"] == new_application["position"]
    assert application["status"] == new_application["status"]
    assert isinstance(application["id"], int)