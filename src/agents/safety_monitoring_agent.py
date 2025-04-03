from typing import Any, Dict
from datetime import datetime, timedelta
from .base_agent import BaseAgent
from ..config.config import settings

class SafetyMonitoringAgent(BaseAgent):
    def __init__(self, agent_id: str):
        super().__init__(agent_id, "SafetyMonitor")
        self.last_movement_time = datetime.now()
        self.sensitivity = settings.FALL_DETECTION_SENSITIVITY
        self.inactivity_threshold = timedelta(
            minutes=settings.INACTIVITY_THRESHOLD_MINUTES
        )
    
    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process movement and activity data.
        
        Args:
            data: Dictionary containing:
                - acceleration (Dict[str, float]): x, y, z acceleration values
                - movement_detected (bool): whether movement was detected
                - timestamp (str): ISO format timestamp
        """
        current_time = datetime.fromisoformat(data["timestamp"])
        alerts = []
        
        # Check for falls using acceleration data
        if "acceleration" in data:
            fall_detected = self._detect_fall(data["acceleration"])
            if fall_detected:
                alerts.append({
                    "type": "fall_detected",
                    "timestamp": current_time.isoformat(),
                    "severity": "high",
                    "acceleration_data": data["acceleration"]
                })
        
        # Update last movement time if movement is detected
        if data.get("movement_detected", False):
            self.last_movement_time = current_time
        
        # Check for inactivity
        inactivity_duration = current_time - self.last_movement_time
        if inactivity_duration > self.inactivity_threshold:
            alerts.append({
                "type": "inactivity",
                "timestamp": current_time.isoformat(),
                "severity": "medium",
                "duration_minutes": inactivity_duration.total_seconds() / 60
            })
        
        return {
            "status": "alert" if alerts else "normal",
            "alerts": alerts,
            "last_movement": self.last_movement_time.isoformat()
        }
    
    async def handle_alert(self, alert_data: Dict[str, Any]) -> bool:
        """Handle safety-related alerts."""
        try:
            alert_type = alert_data["type"]
            severity = alert_data["severity"]
            
            # Generate alert message using Ollama
            prompt = f"""
            Generate a clear and urgent safety alert message for:
            - Type: {alert_type}
            - Severity: {severity}
            - Time: {alert_data['timestamp']}
            Make it clear and actionable for caregivers.
            """
            
            alert_message = await self.query_ollama(prompt)
            
            # Log the alert
            self.log_activity(
                f"Safety Alert - {alert_type}: {alert_message}",
                level="warning" if severity != "high" else "error"
            )
            
            # Here we would implement the actual alert sending logic
            # (e.g., notifying emergency contacts, caregivers)
            
            return True
        except Exception as e:
            self.log_activity(f"Error handling alert: {str(e)}", level="error")
            return False
    
    def _detect_fall(self, acceleration: Dict[str, float]) -> bool:
        """
        Detect falls using acceleration data.
        Basic implementation - could be enhanced with more sophisticated algorithms.
        """
        # Calculate total acceleration magnitude
        total_acceleration = (
            acceleration["x"]**2 +
            acceleration["y"]**2 +
            acceleration["z"]**2
        )**0.5
        
        # Threshold for fall detection (can be adjusted based on sensitivity)
        fall_threshold = 32.0 * self.sensitivity  # typical value for falls
        
        return total_acceleration > fall_threshold 