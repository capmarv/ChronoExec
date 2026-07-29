from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import models
from dependencies import get_db
from schemas import JobCreate

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])


#to create a job
@router.post("")
async def create_job(model: JobCreate, db: Session = Depends(get_db)):

    db_jobs = models.Jobs(job_name=model.job_name,
                          job_description=model.job_description,
                          job_command=model.job_command,
                          job_scheduled_time=model.job_scheduled_time,
                          job_status=model.job_status)

    db.add(db_jobs)
    db.commit()
    db.refresh(db_jobs)


#to get all jobs that are stored
@router.get("/all")
async def get_all_jobs(db: Session = Depends(get_db)):
    db_jobs = db.query(models.Jobs).all()

    if not db_jobs:
        raise HTTPException(status_code= 404, detail = "No Jobs Found")

    return db_jobs


#to get a specific job through id
@router.get("/{job_id}")
async def get_job(job_id: int, db: Session = Depends(get_db)):
    db_job = db.query(models.Jobs).filter(models.Jobs.job_id == job_id).first()

    if not db_job:
        raise HTTPException(status_code= 404, detail = "Job not found")

    return db_job


#to pause a job
@router.patch("/{job_id}/pause")
async def patch_job(job_id: int, db: Session = Depends(get_db)):
    db_job = db.query(models.Jobs).filter(models.Jobs.job_id == job_id).first()

    if not db_job:
        raise HTTPException(status_code= 404, detail = "Job Not Found")

    if db_job.job_status == "COMPLETED":
        raise HTTPException(status_code=400, detail="Completed jobs cannot be paused")

    if db_job.job_status == "PAUSED":
        raise HTTPException(status_code=400, detail="Job is already paused")

    db_job.job_status = "PAUSED"
    db.commit()

    return {"message" : "Job Paused"}


#to resume a job
@router.patch("/resume/{job_id}")
async def resume_job(job_id: int, db: Session = Depends(get_db)):
    db_job = db.query(models.Jobs).filter(models.Jobs.job_id == job_id).first()

    if not db_job:
        raise HTTPException(status_code= 404, detail = "Job Not Found")

    if db_job.job_status == "COMPLETED":
        raise HTTPException(status_code=400, detail="Job is already completed")

    if db_job.job_status == "ACTIVE":
        raise HTTPException(status_code=400, detail="Job is already active")

    db_job.job_status = "ACTIVE"
    db.commit()
    return {"message" : "Job Resumed and now is active."}


#to update a job
@router.put("/{job_id}")
async def update_job(job_id: int, model: JobCreate,db: Session = Depends(get_db)):
    db_job = db.query(models.Jobs).filter(models.Jobs.job_id == job_id).first()

    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")

    db_job.job_name = model.job_name
    db_job.job_description = model.job_description
    db_job.job_command = model.job_command
    db_job.job_scheduled_time = model.job_scheduled_time
    db_job.job_status = model.job_status

    db.commit()
    db.refresh(db_job)

    return db_job

#to delete a job
@router.delete("/{job_id}")
async def delete_job(job_id:int, db: Session = Depends(get_db)):
    db_job = db.query(models.Jobs).filter(models.Jobs.job_id == job_id).first()

    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")

    db.delete(db_job)
    db.commit()

    return {"message" : "Job deleted"}
