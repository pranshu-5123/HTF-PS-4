# Elderly Care Multi-Agent AI System

A comprehensive multi-agent AI system designed to assist elderly individuals living independently by providing real-time monitoring, reminders, and safety alerts.

## Features

- **Health Monitoring Agent**
  - Monitors vital signs (heart rate, blood pressure, glucose levels)
  - Generates alerts for abnormal health metrics
  - Uses Ollama's Mistral model for generating context-aware health alerts

- **Safety Monitoring Agent**
  - Tracks movement and detects falls using acceleration data
  - Monitors activity levels and alerts for unusual inactivity
  - Provides real-time safety alerts

- **Reminder Agent**
  - Manages medication schedules and appointments
  - Sends daily activity reminders
  - Generates personalized reminder messages using AI

## System Architecture

The system is built using Python with FastAPI for the backend API. It utilizes a multi-agent architecture where each agent is responsible for specific aspects of elderly care:

```
elderly_care_system/
├── src/
│   ├── agents/
│   │   ├── base_agent.py
│   │   ├── health_monitoring_agent.py
│   │   ├── safety_monitoring_agent.py
│   │   └── reminder_agent.py
│   ├── api/
│   │   └── main.py
│   ├── config/
│   │   └── config.py
│   └── utils/
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd elderly_care_system
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Make sure Ollama is installed and the Mistral model is available:
```bash
ollama pull mistral
```

## Usage

1. Start the FastAPI server:
```bash
uvicorn src.api.main:app --reload
```

2. The API will be available at `http://localhost:8000`

3. API Endpoints:
   - `POST /health/monitor`: Submit health metrics for monitoring
   - `POST /safety/monitor`: Submit movement and safety data
   - `POST /reminder/schedule`: Schedule a new reminder
   - `POST /reminder/process`: Process current reminders
   - `GET /system/status`: Check system status

## API Examples

### Monitor Health Metrics
```bash
curl -X POST "http://localhost:8000/health/monitor" \
     -H "Content-Type: application/json" \
     -d '{
       "heart_rate": 75,
       "blood_pressure_systolic": 120,
       "blood_pressure_diastolic": 80,
       "glucose_level": 100,
       "timestamp": "2024-03-15T10:00:00"
     }'
```

### Monitor Safety
```bash
curl -X POST "http://localhost:8000/safety/monitor" \
     -H "Content-Type: application/json" \
     -d '{
       "acceleration": {"x": 0.1, "y": 0.2, "z": 9.8},
       "movement_detected": true,
       "timestamp": "2024-03-15T10:00:00"
     }'
```

### Schedule Reminder
```bash
curl -X POST "http://localhost:8000/reminder/schedule" \
     -H "Content-Type: application/json" \
     -d '{
       "activity": "Take blood pressure medication",
       "scheduled_time": "2024-03-15T10:00:00"
     }'
```

## Configuration

The system can be configured by modifying the settings in `src/config/config.py`:
- Health monitoring thresholds
- Fall detection sensitivity
- Inactivity threshold
- Reminder schedules
- Alert settings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 