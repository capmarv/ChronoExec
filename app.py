from fastapi import FastAPI
from database import engine
import models
from routers.jobs import router
from scheduler import start_scheduler

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(router)

start_scheduler()