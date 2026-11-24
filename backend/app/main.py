
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import engine, Base, get_db
from app.models.job import Job
from app.schemas.job import JobResponse


app = FastAPI(
    title="JobFinder API",
    description="Álláskereső alkalmazás API-ja",
    version="0.1.0"
)

Base.metadata.create_all(bind=engine)

# Engedélyezzük a React frontend hozzáférését
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "JobFinder API is running!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.get("/jobs", response_model=list[JobResponse])
def get_jobs(db: Session = Depends(get_db)):
    statement = select(Job).where(Job.is_active == True)
    jobs = db.scalars(statement).all()
    return jobs
