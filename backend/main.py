from fastapi import FastAPI
from fastapi import HTTPException

from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import FileResponse

from fastapi.responses import StreamingResponse

from fastapi.staticfiles import StaticFiles

from pathlib import Path
import json

from .agent import (
    vc_scout,
    vc_scout_stream,
    monitor_platforms,
    monitor_platforms_stream,
    trend_detection,
    trend_detection_stream,
    startup_discovery,
    startup_discovery_stream,
    founder_interview,
    founder_interview_stream,
    investment_memo,
    investment_memo_stream,
    spam_score,
    SPAM_THRESHOLD,
)

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





class TopicRequest(BaseModel):

    topic: str





class SectorRequest(BaseModel):

    sector: str





class FounderRequest(BaseModel):

    founder: str





class CompanyRequest(BaseModel):

    company: str





class MonitorRequest(BaseModel):

    query: str


class SourceItem(BaseModel):

    name: str
    url: str
    enabled: bool


class SourcesPayload(BaseModel):

    rss: list[SourceItem]
    github: dict


SOURCES_PATH = Path(__file__).resolve().parent / "sources.json"



frontend_dir = Path(__file__).resolve().parent.parent / "frontend"



if frontend_dir.is_dir():

    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")



    @app.get("/")

    def index():

        return FileResponse(str(frontend_dir / "index.html"))



@app.post("/scout")

def scout(data: RequestData):

    score, reasons = spam_score(data.goal)
    if score >= SPAM_THRESHOLD:
        raise HTTPException(status_code=400, detail=f"Blocked input (spam score {score}): {', '.join(reasons) or 'high risk'}")
    try:
        return StreamingResponse(vc_scout_stream(data.goal), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Model error: {e}")





@app.post("/monitor")

def monitor(data: MonitorRequest):

    score, reasons = spam_score(data.query)
    if score >= SPAM_THRESHOLD:
        raise HTTPException(status_code=400, detail=f"Blocked input (spam score {score}): {', '.join(reasons) or 'high risk'}")
    try:
        return StreamingResponse(monitor_platforms_stream(data.query), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Monitor error: {e}")





@app.post("/trend")

def trend(data: TopicRequest):

    score, reasons = spam_score(data.topic)
    if score >= SPAM_THRESHOLD:
        raise HTTPException(status_code=400, detail=f"Blocked input (spam score {score}): {', '.join(reasons) or 'high risk'}")
    try:
        return StreamingResponse(trend_detection_stream(data.topic), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Trend error: {e}")





@app.post("/discover")

def discover(data: SectorRequest):

    score, reasons = spam_score(data.sector)
    if score >= SPAM_THRESHOLD:
        raise HTTPException(status_code=400, detail=f"Blocked input (spam score {score}): {', '.join(reasons) or 'high risk'}")
    try:
        return StreamingResponse(startup_discovery_stream(data.sector), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Discover error: {e}")


@app.post("/interview")

def interview(data: FounderRequest):

    score, reasons = spam_score(data.founder)
    if score >= SPAM_THRESHOLD:
        raise HTTPException(status_code=400, detail=f"Blocked input (spam score {score}): {', '.join(reasons) or 'high risk'}")
    try:
        return StreamingResponse(founder_interview_stream(data.founder), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Interview error: {e}")


@app.post("/memo")

def memo(data: CompanyRequest):

    score, reasons = spam_score(data.company)
    if score >= SPAM_THRESHOLD:
        raise HTTPException(status_code=400, detail=f"Blocked input (spam score {score}): {', '.join(reasons) or 'high risk'}")
    try:
        return StreamingResponse(investment_memo_stream(data.company), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Memo error: {e}")


@app.get("/sources")
def get_sources():
    if SOURCES_PATH.is_file():
        return json.loads(SOURCES_PATH.read_text())
    return {
        "rss": [
            {"name": "Hacker News", "url": "https://hnrss.org/frontpage", "enabled": True},
            {"name": "TechCrunch", "url": "https://techcrunch.com/feed/", "enabled": True},
            {"name": "The Verge", "url": "https://www.theverge.com/rss/index.xml", "enabled": True},
        ],
        "github": {"enabled": True},
    }


@app.post("/sources")
def update_sources(payload: SourcesPayload):
    data = payload.model_dump()
    SOURCES_PATH.write_text(json.dumps(data, indent=2))
    return {"ok": True}
