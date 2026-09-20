from fastapi.testclient import TestClient
from app import main
import pytest

client = TestClient(main.app)

@pytest.fixture
def reset_apps():
    main.applications[:] = main.get_default_applications()
    yield

def test_get_one_application(reset_apps):
    response = client.get("/applications/1")
    data = response.json()
    application = data["application"]
    assert response.status_code == 200
    assert application["id"] == 1
    assert application["company"] == "Company A"
    assert application["status"] == "Applied"

def test_get_application_not_found(reset_apps):
    response = client.get("/applications/99")
    assert response.status_code == 404
    assert response.json() == {"detail": "Application not found"}

def test_create_application(reset_apps):
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

def test_update_application(reset_apps):
    update = {
        "status": "Offer Given"
    }

    response = client.patch("/applications/1", json=update)
    data = response.json()
    application  = data["application"]
    assert response.status_code == 200
    assert application["company"] == "Company A"
    assert application["position"] == "Software Dev"
    assert application["status"] == "Offer Given"

def test_delete_application(reset_apps):
    response = client.delete("/applications/3")
    assert response.status_code == 200
    assert response.json() == {"message": "Application deleted successfully"}
    response = client.get("/applications/3")
    assert response.status_code == 404
    assert response.json() == {"detail": "Application not found"}

def test_create_application_missing_fields(reset_apps):
    new_application = {
        "company" : "Apple",
        "status" : "Interview"
    }

    response = client.post("/applications", json=new_application)
    assert response.status_code == 422

def test_patch_application_notfound(reset_apps):
    update = {
            "status": "Offer Given"
    }

    response = client.patch("/applications/99", json=update)
    assert response.status_code == 404
    assert response.json() == {"detail": "Application not found"}

def test_delete_application_notfound(reset_apps):
    response = client.delete("/applications/99")
    assert response.status_code == 404
    assert response.json() == {"detail": "Application not found"}

def test_get_applications(reset_apps):
    response = client.get("/applications")
    data = response.json()
    assert "applications" in data
    applications = data["applications"]
    assert response.status_code == 200
    assert len(applications) == 3
    assert applications[0]["company"] == "Company A"

def test_create_application_missing_fields_not_modified(reset_apps):
    new_application = {
        "company" : "Apple",
        "status" : "Interview"
    }

    response = client.post("/applications", json=new_application)
    assert response.status_code == 422
    response = client.get("/applications")
    assert response.status_code == 200
    data = response.json()
    applications = data["applications"]
    assert len(applications) == 3
