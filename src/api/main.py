from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime
import uuid
import os

from ..agents.health_monitoring_agent import HealthMonitoringAgent
from ..agents.safety_monitoring_agent import SafetyMonitoringAgent
from ..agents.reminder_agent import ReminderAgent
from ..utils.data_processor import DataProcessor
from ..models.data_models import HealthData, SafetyData, ReminderData

app = FastAPI(title="Elderly Care Multi-Agent System")

# Initialize agents
health_agent = HealthMonitoringAgent(agent_id=str(uuid.uuid4()))
safety_agent = SafetyMonitoringAgent(agent_id=str(uuid.uuid4()))
reminder_agent = ReminderAgent(agent_id=str(uuid.uuid4()))

# Initialize data processor
data_processor = DataProcessor()

# Request/Response Models
class HealthDataRequest(BaseModel):
    heart_rate: float
    blood_pressure_systolic: float
    blood_pressure_diastolic: float
    glucose_level: Optional[float] = None
    timestamp: str

class MovementDataRequest(BaseModel):
    acceleration: Dict[str, float]
    movement_detected: bool
    timestamp: str

class ReminderDataRequest(BaseModel):
    activity: str
    scheduled_time: str

class AlertResponse(BaseModel):
    status: str
    alerts: List[Dict]
    agent_type: str
    timestamp: str

@app.get("/")
async def root():
    return {"message": "Welcome to Elderly Care Multi-Agent System API"}

@app.get("/data/health")
async def get_health_data():
    """Load and return health monitoring data from CSV"""
    try:
        data = data_processor.load_health_data("DataSet/health_monitoring.csv")
        return {"status": "success", "data": [d.dict() for d in data[:10]]}  # Return first 10 records
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/data/safety")
async def get_safety_data():
    """Load and return safety monitoring data from CSV"""
    try:
        data = data_processor.load_safety_data("DataSet/safety_monitoring.csv")
        return {"status": "success", "data": [d.dict() for d in data[:10]]}  # Return first 10 records
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/data/reminders")
async def get_reminder_data():
    """Load and return reminder data from CSV"""
    try:
        data = data_processor.load_reminder_data("DataSet/daily_reminder.csv")
        return {"status": "success", "data": [d.dict() for d in data[:10]]}  # Return first 10 records
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/health/monitor", response_model=AlertResponse)
async def monitor_health(data: HealthDataRequest):
    """Monitor health metrics and generate alerts if necessary."""
    try:
        result = await health_agent.process(data.dict())
        return {
            **result,
            "agent_type": "health",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/safety/monitor", response_model=AlertResponse)
async def monitor_safety(data: MovementDataRequest):
    """Monitor movement and safety, detecting falls and inactivity."""
    try:
        result = await safety_agent.process(data.dict())
        return {
            **result,
            "agent_type": "safety",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reminder/schedule", response_model=Dict)
async def schedule_reminder(data: ReminderDataRequest):
    """Schedule a new reminder for an activity."""
    try:
        scheduled_time = datetime.fromisoformat(data.scheduled_time)
        success = reminder_agent.schedule_reminder(
            data.activity,
            scheduled_time
        )
        return {
            "status": "success" if success else "error",
            "message": f"Reminder scheduled for {data.activity}",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reminder/process", response_model=AlertResponse)
async def process_reminders():
    """Process current reminders and generate necessary alerts."""
    try:
        current_time = datetime.now()
        result = await reminder_agent.process({
            "current_time": current_time.isoformat(),
            "reminders": reminder_agent.scheduled_reminders
        })
        return {
            **result,
            "agent_type": "reminder",
            "timestamp": current_time.isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/system/status")
async def get_system_status():
    """Get the current status of all agents in the system."""
    return {
        "status": "operational",
        "agents": {
            "health": {"id": health_agent.agent_id, "type": health_agent.agent_type},
            "safety": {"id": safety_agent.agent_id, "type": safety_agent.agent_type},
            "reminder": {"id": reminder_agent.agent_id, "type": reminder_agent.agent_type}
        },
        "timestamp": datetime.now().isoformat()
    } 