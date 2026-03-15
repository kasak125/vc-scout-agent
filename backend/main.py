from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from agent import vc_scout
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RequestData(BaseModel):
    goal: str

frontend_dir = Path(__file__).resolve().parent.parent / "frontend"

if frontend_dir.is_dir():
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")

    @app.get("/")
    def index():
        return FileResponse(str(frontend_dir / "index.html"))

@app.post("/scout")
def scout(data: RequestData):
    result = vc_scout(data.goal)
    return {"result": result}
