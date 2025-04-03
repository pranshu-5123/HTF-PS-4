import pandas as pd
from datetime import datetime
from typing import List, Dict, Any
from ..models.data_models import HealthData, SafetyData, ReminderData

class DataProcessor:
    @staticmethod
    def load_health_data(file_path: str) -> List[HealthData]:
        df = pd.read_csv(file_path)
        health_data = []
        for _, row in df.iterrows():
            try:
                data = HealthData(
                    device_id=row['Device-ID/User-ID'],
                    timestamp=datetime.strptime(row['Timestamp'], '%m/%d/%Y %H:%M'),
                    heart_rate=float(row['Heart Rate']),
                    heart_rate_threshold=row['Heart Rate Below/Above Threshold (Yes/No)'] == 'Yes',
                    blood_pressure=row['Blood Pressure'],
                    blood_pressure_threshold=row['Blood Pressure Below/Above Threshold (Yes/No)'] == 'Yes',
                    glucose_levels=float(row['Glucose Levels']),
                    glucose_threshold=row['Glucose Levels Below/Above Threshold (Yes/No)'] == 'Yes',
                    oxygen_saturation=float(row['Oxygen Saturation (SpO₂%)']),
                    oxygen_threshold=row['SpO₂ Below Threshold (Yes/No)'] == 'Yes',
                    alert_triggered=row['Alert Triggered (Yes/No)'] == 'Yes',
                    caregiver_notified=row['Caregiver Notified (Yes/No)'] == 'Yes'
                )
                health_data.append(data)
            except Exception as e:
                print(f"Error processing health data row: {e}")
        return health_data

    @staticmethod
    def load_safety_data(file_path: str) -> List[SafetyData]:
        df = pd.read_csv(file_path)
        safety_data = []
        for _, row in df.iterrows():
            try:
                data = SafetyData(
                    device_id=row['Device-ID/User-ID'],
                    timestamp=datetime.strptime(row['Timestamp'], '%m/%d/%Y %H:%M'),
                    movement_activity=row['Movement Activity'],
                    fall_detected=row['Fall Detected (Yes/No)'] == 'Yes',
                    impact_force_level=row['Impact Force Level'] if pd.notna(row['Impact Force Level']) else None,
                    inactivity_duration=int(row['Post-Fall Inactivity Duration (Seconds)']),
                    location=row['Location'],
                    alert_triggered=row['Alert Triggered (Yes/No)'] == 'Yes',
                    caregiver_notified=row['Caregiver Notified (Yes/No)'] == 'Yes'
                )
                safety_data.append(data)
            except Exception as e:
                print(f"Error processing safety data row: {e}")
        return safety_data

    @staticmethod
    def load_reminder_data(file_path: str) -> List[ReminderData]:
        df = pd.read_csv(file_path)
        reminder_data = []
        for _, row in df.iterrows():
            try:
                data = ReminderData(
                    device_id=row['Device-ID/User-ID'],
                    timestamp=datetime.strptime(row['Timestamp'], '%m/%d/%Y %H:%M'),
                    reminder_type=row['Reminder Type'],
                    scheduled_time=datetime.strptime(row['Scheduled Time'], '%H:%M:%S'),
                    reminder_sent=row['Reminder Sent (Yes/No)'] == 'Yes',
                    acknowledged=row['Acknowledged (Yes/No)'] == 'Yes'
                )
                reminder_data.append(data)
            except Exception as e:
                print(f"Error processing reminder data row: {e}")
        return reminder_data 