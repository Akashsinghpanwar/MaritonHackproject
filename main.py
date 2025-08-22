from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from sami.app.rag import add_files, query
from sami.app.tools.distance import distance_nm, eta_days
from sami.app.tools.laytime import compute_laytime, CP, Event
from sami.app.tools.weather import forecast_latlon
from sami.app.settings import UPLOAD_DIR
from sami.app.supabase_client import supabase

app = FastAPI(
    title="Maritime Virtual Assistant API",
    description="An API for a maritime virtual assistant.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# --- Pydantic Models ---

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    citations: List[str]

class UploadStatus(BaseModel):
    ingested_files: List[str]

class DistanceRequest(BaseModel):
    from_lat: float
    from_lon: float
    to_lat: float
    to_lon: float
    speed_knots: float

class DistanceResponse(BaseModel):
    distance_nm: float
    eta_days: float

class LaytimeEvent(BaseModel):
    start: datetime
    end: datetime
    reason: str
    excepted: bool

class LaytimeRequest(BaseModel):
    laytime_hours: float
    demurrage_per_day: float
    despatch_per_day: float
    events: List[LaytimeEvent]

class LaytimeResponse(BaseModel):
    used_hours: float
    demurrage_usd: float
    despatch_usd: float

class WeatherResponse(BaseModel):
    forecast: dict

# --- API Endpoints ---

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Get an answer from the RAG model."""
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    answer, cites = query(request.question.strip())
    return ChatResponse(answer=answer, citations=cites)

@app.post("/upload", response_model=UploadStatus)
async def upload_files(files: List[UploadFile] = File(...)):
    """Upload and ingest documents."""
    copied_paths = []
    for file in files:
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        try:
            # Insert metadata into Supabase
            data, count = supabase.table('documents').insert({"filename": file.filename}).execute()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save document metadata: {e}")

        copied_paths.append(str(file_path))

    try:
        _, ingested = add_files(copied_paths)
        return UploadStatus(ingested_files=[p.split('/')[-1] for p in ingested])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/tools/distance", response_model=DistanceResponse)
async def distance_tool(request: DistanceRequest):
    """Calculate distance and ETA."""
    dist = distance_nm(request.from_lat, request.from_lon, request.to_lat, request.to_lon)
    days = eta_days(dist, request.speed_knots)
    return DistanceResponse(distance_nm=dist, eta_days=days)

@app.post("/tools/laytime", response_model=LaytimeResponse)
async def laytime_tool(request: LaytimeRequest):
    """Calculate laytime."""
    cp = CP(
        laytime_hours=request.laytime_hours,
        demurrage_per_day=request.demurrage_per_day,
        despatch_per_day=request.despatch_per_day,
    )
    events = [Event(**e.dict()) for e in request.events]
    used_h, dem, desp = compute_laytime(cp, events)
    return LaytimeResponse(used_hours=used_h, demurrage_usd=dem, despatch_usd=desp)

@app.get("/tools/weather", response_model=WeatherResponse)
async def weather_tool(lat: float, lon: float):
    """Get weather forecast."""
    forecast = forecast_latlon(lat, lon)
    if "error" in forecast:
        raise HTTPException(status_code=500, detail=forecast["error"])
    return WeatherResponse(forecast=forecast)
