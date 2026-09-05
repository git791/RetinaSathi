from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import screening
from app.config import settings

app = FastAPI(title="RetinaSathi API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.allowed_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(screening.router)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "retinasathi-backend",
        "matlab": "not_connected" if settings.matlab_mode != "compiled" else "compiled"
    }
