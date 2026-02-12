# 🦘 KangarooTracker.io

🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘  

A real-time kangaroo tracking simulation across Australia with a live interactive map, streaming movement data, and replayable paths.

---

## 🌏 Project Overview

**KangarooTracker.io** is a full-stack simulation platform that models kangaroo movement in real time across Australia.

### 🧠 Backend
- Generates or ingests kangaroo position updates every few seconds  
- Estimates short movement routes  
- Exposes data via:
  - WebSocket API  
  - HTTP endpoints  

### 🗄️ Database
- Stores:
  - Animal profiles  
  - Position history  
  - Tracks and paths  
- Enables replay and movement analysis  

### 🗺️ Frontend
- Interactive map of Australia
- Real-time animated kangaroo movement
- Visual features:
  - Movement trails
  - Speed indicators
  - Filters (region, herd, time window)

### 📊 Data
For this project, movement data is simulated but can be based on:
- Real kangaroo range maps
- Open geographic datasets
- Probabilistic movement patterns

🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘  

##  MVP (Minimal Viable Product)

### Core Features
- 🗺️ Map UI centered on Australia  
- 🦘 10–50 simulated kangaroos displaying:
  - Current position
  - Recent path (polyline)
  - Metadata:
    - ID
    - Name
    - Speed

### Real-Time Movement
- Backend pushes updated coordinates every few seconds  
- Frontend animates markers and trails live  

### Controls
- Start / Stop simulation  
- Speed options:
  - 1×
  - 2×
  - 5×
- Toggle:
  - Heatmap view
  - Individual tracks

🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘  


🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘🦘  

# ⚙️ Technical Setup

## 🐍 Backend (FastAPI)

### Install
```bash
mkdir kangaroo-tracker-backend
cd kangaroo-tracker-backend

python3 -m venv .venv
source .venv/bin/activate   # macOS / zsh

pip install fastapi "uvicorn[standard]"
pip freeze > requirements.txt


