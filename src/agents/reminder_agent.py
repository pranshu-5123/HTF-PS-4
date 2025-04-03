from typing import Any, Dict, List
from datetime import datetime, timedelta
from .base_agent import BaseAgent
from ..config.config import settings

class ReminderAgent(BaseAgent):
    def __init__(self, agent_id: str):
        super().__init__(agent_id, "ReminderAgent")
        self.reminder_times = settings.DAILY_REMINDER_TIMES
        self.advance_notice = timedelta(
            minutes=settings.REMINDER_ADVANCE_NOTICE_MINUTES
        )
        self.scheduled_reminders: List[Dict[str, Any]] = []
    
    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process reminder data and schedule.
        
        Args:
            data: Dictionary containing:
                - current_time (str): ISO format timestamp
                - reminders (List[Dict]): list of scheduled reminders
                - activities (List[Dict]): list of daily activities
        """
        current_time = datetime.fromisoformat(data["current_time"])
        upcoming_reminders = []
        alerts = []
        
        # Process scheduled reminders
        for reminder in data.get("reminders", []):
            reminder_time = datetime.fromisoformat(reminder["time"])
            time_until_reminder = reminder_time - current_time
            
            if time_until_reminder <= self.advance_notice:
                alerts.append({
                    "type": "upcoming_reminder",
                    "activity": reminder["activity"],
                    "scheduled_time": reminder_time.isoformat(),
                    "severity": "low"
                })
            elif time_until_reminder > timedelta(0):
                upcoming_reminders.append(reminder)
        
        # Check daily activities
        current_time_str = current_time.strftime("%H:%M")
        if current_time_str in self.reminder_times:
            alerts.append({
                "type": "daily_check",
                "time": current_time.isoformat(),
                "severity": "low"
            })
        
        return {
            "status": "alert" if alerts else "normal",
            "alerts": alerts,
            "upcoming_reminders": upcoming_reminders
        }
    
    async def handle_alert(self, alert_data: Dict[str, Any]) -> bool:
        """Handle reminder-related alerts."""
        try:
            alert_type = alert_data["type"]
            
            if alert_type == "upcoming_reminder":
                activity = alert_data["activity"]
                scheduled_time = datetime.fromisoformat(
                    alert_data["scheduled_time"]
                ).strftime("%H:%M")
                
                # Generate reminder message using Ollama
                prompt = f"""
                Generate a friendly reminder message for:
                Activity: {activity}
                Scheduled Time: {scheduled_time}
                Make it encouraging and clear.
                """
                
                reminder_message = await self.query_ollama(prompt)
                
            elif alert_type == "daily_check":
                # Generate daily check message
                prompt = """
                Generate a friendly message for daily activity check-in.
                Include asking about meals, medication, and general well-being.
                Make it conversational and caring.
                """
                
                reminder_message = await self.query_ollama(prompt)
            
            # Log the reminder
            self.log_activity(
                f"Reminder - {alert_type}: {reminder_message}",
                level="info"
            )
            
            # Here we would implement the actual reminder sending logic
            # (e.g., voice notes, notifications)
            
            return True
        except Exception as e:
            self.log_activity(f"Error handling reminder: {str(e)}", level="error")
            return False
    
    def schedule_reminder(self, activity: str, time: datetime) -> bool:
        """Schedule a new reminder."""
        try:
            self.scheduled_reminders.append({
                "activity": activity,
                "time": time.isoformat(),
                "created_at": datetime.now().isoformat()
            })
            
            self.log_activity(
                f"Scheduled reminder for {activity} at {time.strftime('%H:%M')}"
            )
            return True
        except Exception as e:
            self.log_activity(
                f"Error scheduling reminder: {str(e)}",
                level="error"
            )
            return False 