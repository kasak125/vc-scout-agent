from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import FileResponse

from fastapi.responses import StreamingResponse

from fastapi.staticfiles import StaticFiles

from pathlib import Path

from agent import (
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



frontend_dir = Path(__file__).resolve().parent.parent / "frontend"



if frontend_dir.is_dir():

    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")



    @app.get("/")

    def index():

        return FileResponse(str(frontend_dir / "index.html"))



@app.post("/scout")

def scout(data: RequestData):

    return StreamingResponse(vc_scout_stream(data.goal), media_type="text/plain")





@app.post("/monitor")

def monitor(data: MonitorRequest):

    return StreamingResponse(monitor_platforms_stream(data.query), media_type="text/plain")





@app.post("/trend")

def trend(data: TopicRequest):

    return StreamingResponse(trend_detection_stream(data.topic), media_type="text/plain")





@app.post("/discover")

def discover(data: SectorRequest):

    return StreamingResponse(startup_discovery_stream(data.sector), media_type="text/plain")


@app.post("/interview")

def interview(data: FounderRequest):

    return StreamingResponse(founder_interview_stream(data.founder), media_type="text/plain")


@app.post("/memo")

def memo(data: CompanyRequest):

    return StreamingResponse(investment_memo_stream(data.company), media_type="text/plain")
