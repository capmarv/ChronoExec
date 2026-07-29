import time
import threading
from datetime import datetime
from executor import execute_command
import models
from database import sessionLocal

def check_jobs():
    while True:
        db = sessionLocal()
        try:
            jobs = db.query(models.Jobs).all()
            #print(f"Found {len(jobs)} jobs")
            for job in jobs:
                if job.job_status != "ACTIVE":
                    continue
                if datetime.now() >= job.job_scheduled_time:
                    print(f"Executing Job {job.job_id}: {job.job_name}")
                    output = execute_command(job.job_command)
                    print(output)
                    job.execution_output = output
                    job.executed_at = datetime.now()
                    job.job_status = "COMPLETED"
                    db.commit()
        finally:
            db.close()

        time.sleep(1)

def start_scheduler():
    thread = threading.Thread(target = check_jobs, daemon=True)
    thread.start()

