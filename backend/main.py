from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.archive import router as archive_router
from app.api.gaps import router as gaps_router
from app.api.lab import router as lab_router
from app.api.neuro import router as neuro_router

app = FastAPI(
    title="Cortex-Sec Local Forge",
    description="Backend API for the Autonomous Local Governance System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# App Routers
app.include_router(archive_router)
app.include_router(gaps_router)
app.include_router(lab_router)
app.include_router(neuro_router)

@app.get("/health")
async def health_check():
    return {"status": "operational", "system": "Cortex-Sec Local Forge"}
