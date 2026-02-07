from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .routes.users import router as user_router
from .database import create_tables

app = FastAPI()

# Initialize database tables on startup
create_tables()

# Enable CORS for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)

# Serve static frontend files
frontend_path = Path(__file__).parent.parent / "frontend"
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
