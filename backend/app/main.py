
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import engine, Base, get_db
from app.models.job import Job
from app.schemas.job import JobResponse, JobCreate


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


@app.post("/jobs", response_model=JobResponse, status_code=201)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    db_job = Job(**job.model_dump())

    db.add(db_job)
    db.commit()
    db.refresh(db_job)

    return db_job


@app.put("/jobs/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int,
    job: JobCreate,
    db: Session = Depends(get_db)
):
    db_job = db.get(Job, job_id)

    if db_job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    job_data = job.model_dump()

    for key, value in job_data.items():
        setattr(db_job, key, value)

    db.commit()
    db.refresh(db_job)

    return db_job

@app.delete("/jobs/{job_id}", response_model=JobResponse)
def delete_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    db_job = db.get(Job, job_id)

    if db_job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    db_job.is_active = False

    db.commit()
    db.refresh(db_job)

    return db_job

@app.patch("/jobs/{job_id}/activate", response_model=JobResponse)
def activate_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    db_job = db.get(Job, job_id)

    if db_job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    db_job.is_active = True

    db.commit()
    db.refresh(db_job)

    return db_job