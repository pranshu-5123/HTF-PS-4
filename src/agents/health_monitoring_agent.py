from typing import Any, Dict
from .base_agent import BaseAgent
from ..config.config import settings

class HealthMonitoringAgent(BaseAgent):
    def __init__(self, agent_id: str):
        super().__init__(agent_id, "HealthMonitor")
        self.thresholds = settings.HEALTH_THRESHOLDS
    
    async def process(self, data: Dict[str, float]) -> Dict[str, Any]:
        """
        Process health data and check for anomalies.
        
        Args:
            data: Dictionary containing health metrics
                 (heart_rate, blood_pressure_systolic, blood_pressure_diastolic, glucose_level)
        """
        alerts = []
        for metric, value in data.items():
            if metric in self.thresholds:
                threshold = self.thresholds[metric]
                if value < threshold["min"] or value > threshold["max"]:
                    alert = {
                        "metric": metric,
                        "value": value,
                        "threshold": threshold,
                        "severity": self._calculate_severity(metric, value, threshold)
                    }
                    alerts.append(alert)
                    self.log_activity(
                        f"Abnormal {metric}: {value} (Threshold: {threshold})",
                        level="warning"
                    )
        
        return {
            "status": "alert" if alerts else "normal",
            "alerts": alerts,
            "data": data
        }
    
    async def handle_alert(self, alert_data: Dict[str, Any]) -> bool:
        """Handle health-related alerts."""
        try:
            severity = alert_data["severity"]
            metric = alert_data["metric"]
            value = alert_data["value"]
            
            # Generate alert message using Ollama
            prompt = f"""
            Generate a clear and concise health alert message for:
            - Metric: {metric}
            - Current Value: {value}
            - Severity: {severity}
            Make it informative but not alarming.
            """
            
            alert_message = await self.query_ollama(prompt)
            
            # Log the alert
            self.log_activity(
                f"Health Alert - {metric}: {alert_message}",
                level="warning"
            )
            
            # Here we would implement the actual alert sending logic
            # (e.g., notifying caregivers, healthcare providers)
            
            return True
        except Exception as e:
            self.log_activity(f"Error handling alert: {str(e)}", level="error")
            return False
    
    def _calculate_severity(self, metric: str, value: float, threshold: Dict[str, float]) -> str:
        """Calculate the severity of the anomaly."""
        min_val, max_val = threshold["min"], threshold["max"]
        
        # Calculate how far the value is from the acceptable range
        if value < min_val:
            deviation = (min_val - value) / min_val
        else:
            deviation = (value - max_val) / max_val
        
        if deviation > 0.5:
            return "high"
        elif deviation > 0.2:
            return "medium"
        else:
            return "low" 