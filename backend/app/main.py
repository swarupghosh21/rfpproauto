from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import engine
from app.models import Base
from app.routers import rfp, prebid
from dotenv import load_dotenv
from app.routes.upload import router as upload_router
from app.routes.process import router as process_router

load_dotenv()
# from app.routers import rfp, queries, prebid

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(rfp.router)
# app.include_router(queries.router)
# app.include_router(prebid.router)
app.include_router(upload_router)
app.include_router(process_router)