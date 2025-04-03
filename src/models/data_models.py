from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class HealthData(BaseModel):
    device_id: str
    timestamp: datetime
    heart_rate: float
    heart_rate_threshold: bool
    blood_pressure: str
    blood_pressure_threshold: bool
    glucose_levels: float
    glucose_threshold: bool
    oxygen_saturation: float
    oxygen_threshold: bool
    alert_triggered: bool
    caregiver_notified: bool

class SafetyData(BaseModel):
    device_id: str
    timestamp: datetime
    movement_activity: str
    fall_detected: bool
    impact_force_level: Optional[str]
    inactivity_duration: int
    location: str
    alert_triggered: bool
    caregiver_notified: bool

class ReminderData(BaseModel):
    device_id: str
    timestamp: datetime
    reminder_type: str
    scheduled_time: datetime
    reminder_sent: bool
    acknowledged: bool 