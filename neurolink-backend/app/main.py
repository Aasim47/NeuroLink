from fastapi import FastAPI
from app.routers import patients
from app.routers import family
from app.routers import memories
from app.routers import routines
from app.routers import alerts
from app.routers import location
from app.routers import voice
from app.routers import debug
from app.routers import photos
from app.routers import safezone
from app.routers import assistant
from app.routers import patient_summary
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="NeuroLink API")

app.include_router(patients.router)
app.include_router(family.router)
app.include_router(memories.router)
app.include_router(routines.router)
app.include_router(alerts.router)
app.include_router(location.router)
app.include_router(voice.router)
app.include_router(debug.router)
app.include_router(photos.router)
app.include_router(safezone.router)
app.include_router(assistant.router)
app.include_router(patient_summary.router)



@app.get("/")
def root():
    return {"message": "NeuroLink Backend Running"}

@app.get("/health")
def health():
    return {"status": "running"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)