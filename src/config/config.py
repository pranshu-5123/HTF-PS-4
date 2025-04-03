from pydantic_settings import BaseSettings
from typing import Dict, List

class Settings(BaseSettings):
    # Ollama Model Configuration
    OLLAMA_MODEL: str = "mistral"
    OLLAMA_API_BASE: str = "http://localhost:11434"
    
    # Health Monitoring Thresholds
    HEALTH_THRESHOLDS: Dict[str, Dict[str, float]] = {
        "heart_rate": {"min": 60, "max": 100},
        "blood_pressure_systolic": {"min": 90, "max": 140},
        "blood_pressure_diastolic": {"min": 60, "max": 90},
        "glucose_level": {"min": 70, "max": 180},
    }
    
    # Activity Monitoring Settings
    INACTIVITY_THRESHOLD_MINUTES: int = 120
    FALL_DETECTION_SENSITIVITY: float = 0.8
    
    # Reminder Settings
    REMINDER_ADVANCE_NOTICE_MINUTES: int = 30
    DAILY_REMINDER_TIMES: List[str] = [
        "08:00",
        "12:00",
        "16:00",
        "20:00"
    ]
    
    # Alert Settings
    EMERGENCY_CONTACTS: List[Dict[str, str]] = []
    ALERT_RETRY_INTERVAL_MINUTES: int = 5
    MAX_ALERT_RETRIES: int = 3

    class Config:
        env_file = ".env"

settings = Settings() 