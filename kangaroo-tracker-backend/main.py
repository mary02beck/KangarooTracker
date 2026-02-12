from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import math
import random
from typing import List, Dict

app = FastAPI()

# Allow local frontend dev (adjust for your frontend port)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rough bounding box for mainland Australia
# Rough inland bounding box for mainland Australia (avoids most coastal water)
MIN_LAT, MAX_LAT = -38.0, -16.0
MIN_LON, MAX_LON = 114.0, 149.0


class Kangaroo(BaseModel):
    id: int
    name: str
    lat: float
    lon: float
    speed_kmh: float


kangaroos: Dict[int, Kangaroo] = {}


def init_kangaroos(n: int = 20) -> None:
    for i in range(n):
        kangaroos[i] = Kangaroo(
            id=i,
            name=f"Kanga-{i}",
            lat=random.uniform(-35.0, -20.0),
            lon=random.uniform(115.0, 150.0),
            speed_kmh=random.uniform(5.0, 25.0),  # rough hopping speed
        )


init_kangaroos()


def move_kangaroos(dt_seconds: float = 5.0) -> None:
    """Very simple random-walk movement within AU bounds."""
    for k_id, k in list(kangaroos.items()):
        distance_km = (k.speed_kmh / 3600.0) * dt_seconds
        # Random heading
        heading = random.uniform(0, 2 * math.pi)
        dlat_km = distance_km * math.cos(heading)
        dlon_km = distance_km * math.sin(heading)

        # Convert km to degrees (very rough, ok for simulation)
        dlat_deg = dlat_km / 111.0
        dlon_deg = dlon_km / (111.0 * math.cos(math.radians(k.lat)))

        new_lat = k.lat + dlat_deg
        new_lon = k.lon + dlon_deg

        # Keep inside AU bounding box
        new_lat = max(MIN_LAT, min(MAX_LAT, new_lat))
        new_lon = max(MIN_LON, min(MAX_LON, new_lon))

        kangaroos[k_id] = k.copy(update={"lat": new_lat, "lon": new_lon})


@app.get("/kangaroos", response_model=List[Kangaroo])
async def list_kangaroos():
    """Initial snapshot for the frontend."""
    return list(kangaroos.values())


@app.websocket("/ws/kangaroos")
async def websocket_kangaroos(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            move_kangaroos()
            await ws.send_json([k.dict() for k in kangaroos.values()])
            await asyncio.sleep(5)  # update every 5 seconds
    except WebSocketDisconnect:
        pass