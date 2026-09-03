from fastapi import FastAPI

app = FastAPI()

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
