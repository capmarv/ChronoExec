from pydantic import BaseModel
from datetime import datetime
from typing import Literal

class JobCreate(BaseModel):
    job_name: str
    job_description: str | None = None
    job_command: str
    job_scheduled_time: datetime
    job_status: Literal["ACTIVE", "PAUSED", "COMPLETED"]
    execution_output: str