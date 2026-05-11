from fastapi import FastAPI
from app.routers import rfp

app = FastAPI()

app.include_router(rfp.router)