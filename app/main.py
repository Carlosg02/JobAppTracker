from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class ApplicationCreate(BaseModel):
    company: str
    position: str
    status: str

class ApplicationUpdate(BaseModel):
    company: Optional[str] = None
    position: Optional[str] = None
    status: Optional[str] = None

@app.get("/")
def root():
    return {"message": "Job application tracker API"}

@app.get("/about")
def about():
    return {"project": "Job Application Tracker",
            "version": "1.0"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

applications = [
        {"id": 1, "company": "Company A", "position": "Software Dev", "status": "Applied"},
        {"id": 2, "company": "Company B", "position": "Data Analyst", "status": "Interview Scheduled"},
        {"id": 3, "company": "Company C", "position": "Project Manager", "status": "Offer Received"}
    ]

@app.get("/applications")
def get_applications():
    return {"applications": applications}

@app.get("/applications/{id}", status_code=200)
def get_applications_by_id(id:int):
    for application in applications:
        if application["id"] == id:
            return {"application": application}
    raise HTTPException(status_code=404, detail="Application not found")

@app.post("/applications", status_code=201)
def create_application(application: ApplicationCreate):
    new_id = max(app["id"] for app in applications) + 1 if applications else 1
    new_application = {
        "id": new_id,
        "company": application.company,
        "position": application.position,
        "status": application.status
    }
    applications.append(new_application)
    return{"application": new_application}

@app.patch("/applications/{id}", status_code=200)
def update_application(id:int, application: ApplicationUpdate):
    for app in applications:
        if app["id"] == id:
            if application.company is not None:
                app["company"]= application.company
            if application.position is not None:
                app["position"] = application.position
            if application.status is not None:
                app["status"] = application.status
            return {"application": app}
    raise HTTPException(status_code=404, detail="Application not found")

@app.delete("/applications/{id}")
def delete_application(id:int):
    for i, app in enumerate(applications):
        if app["id"] == id:
            del applications[i]
            return {"message": "Application deleted successfully"}
    raise HTTPException(status_code=404, detail="Application not found")
