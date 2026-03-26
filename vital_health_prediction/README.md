## Project Overview

**VitalHealth AI** is an intelligent health monitoring system that combines real-time sensor data with machine learning to predict cardiovascular risk and provide personalized health recommendations. The system uses three biomedical sensors connected to an ESP32 microcontroller and a Flask-based web application with a Gradient Boosting ML model trained on over 200,000 patient records.

**Key Achievements:**
- 94% model accuracy in predicting cardiovascular risk
- 99.9% recall rate - catches almost all high-risk cases
- Real-time monitoring with updates every 3-5 seconds
- AI chatbot for personalized health guidance
- Comprehensive PDF reports for medical consultations

---

## Features

**Core Features**
- Real-time health monitoring using ESP32 sensors (MAX30102, MLX90614, AD8232)
- AI-powered cardiovascular risk prediction using Gradient Boosting model
- ECG waveform visualization in real-time
- Personalized health recommendations based on user profile and vitals
- Intelligent chatbot assistant for health queries and wellness guidance
- Professional PDF report generation for medical consultations
- Health trends analytics with beautiful charts and visualizations
- Real-time alerts for critical vital signs

**User Features**
- Secure user authentication with login and registration
- Complete health profile management (age, gender, height, weight, lifestyle factors)
- Medical conditions tracking with severity levels (hypertension, diabetes, heart disease, asthma, etc.)
- Prediction history with trend analysis
- Downloadable health reports in PDF format

**Technical Features**
- RESTful API for sensor data and predictions
- SQLite database for user data and health records
- Responsive design for desktop, tablet, and mobile devices
- WebSocket support for real-time data streaming

---

## Technology Stack

**Backend**
- Python 3.8+ with Flask framework
- Flask-Login for user authentication
- Flask-SQLAlchemy for database ORM
- scikit-learn and XGBoost for machine learning
- joblib for model serialization

**Frontend**
- Bootstrap 5 for responsive UI
- Chart.js for data visualization
- Font Awesome for icons
- HTML5, CSS3, JavaScript

**Hardware**
- ESP32 microcontroller
- MAX30102 for heart rate and SpO₂
- MLX90614 for non-contact temperature
- AD8232 for ECG signal

**Database**
- SQLite for lightweight local storage

---

## Hardware Connections

**MAX30102 (Heart Rate & SpO₂)**
- VIN → 3.3V
- GND → GND
- SDA → GPIO 21
- SCL → GPIO 20

**MLX90614 (Temperature)**
- VIN → 3.3V
- GND → GND
- SDA → GPIO 21 (shared)
- SCL → GPIO 20 (shared)

**AD8232 (ECG)**
- 3.3V → 3.3V
- GND → GND
- OUTPUT → GPIO 34
- LO+ → GPIO 35
- LO- → GPIO 32

**ECG Electrode Placement**
- Red wire (RA): Right arm/wrist
- Yellow wire (LA): Left arm/wrist
- Green wire (RL): Right leg/ankle

---

## Installation Guide

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/vitalhealth-ai.git
cd vitalhealth-ai
```

**2. Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**3. Install Python dependencies**
```bash
pip install -r requirements.txt
pip install reportlab matplotlib seaborn pandas numpy xgboost scikit-learn
```

**4. Initialize database**
```bash
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('Database created!')"
```

**5. Run the application**
```bash
python run.py
```

**6. Access the application**
Open browser and go to `http://localhost:5000`

---

## ESP32 Setup

**1. Install Arduino ESP32 Board**
- Open Arduino IDE → File → Preferences
- Add to Additional Boards Manager URLs: `https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json`
- Tools → Board → Boards Manager → Search "ESP32" → Install

**2. Install Required Libraries**
- MAX30105 by SparkFun
- Adafruit MLX90614 Library
- ArduinoJson by Benoit Blanchon

**3. Configure WiFi Credentials**
Open `esp32_code/esp32_sender.ino` and update:
```cpp
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* serverUrl = "http://YOUR_COMPUTER_IP:5000/api/sensor-data";
```

**4. Upload Code**
- Connect ESP32 via USB
- Select correct board and port
- Click Upload button

---

## Usage Guide

**Register Account**
- Click Register on homepage
- Fill username, email, password
- Enter age, gender, height, weight
- Select lifestyle factors (smoking, alcohol, exercise)
- Choose medical conditions with severity levels
- Submit to create health profile

**Make a Prediction**
- Navigate to Predict page
- Enter heart rate (60-100 BPM)
- Enter SpO₂ (95-100%)
- Enter temperature (36.1-37.2°C)
- Click Analyze Health Risk
- View risk level, confidence score, and recommendations

**Live Monitoring**
- Go to Live Data page
- Click Start Demo or connect to ESP32
- Watch real-time vital signs update
- See automatic AI predictions with every reading
- Observe ECG waveform visualization

**AI Chatbot**
- Navigate to AI Chat
- Ask questions about stress, sleep, heart health, diet, exercise
- Get personalized health advice and wellness tips
- Request health summary to see profile insights

**View Health Trends**
- Go to Trends page
- View heart rate, SpO₂, and temperature trend charts
- See risk distribution pie chart
- Review summary statistics and health insights

**Generate Report**
- From Dashboard, click Download Report
- PDF includes patient information, lifestyle profile, medical conditions, vital signs summary, recent records, health assessments, and personalized recommendations

---

## API Endpoints

**Authentication**
- `/auth/register` (POST) - Register new user
- `/auth/login` (POST) - User login
- `/auth/logout` (GET) - Logout user

**Main Routes**
- `/` - Landing page
- `/dashboard` - User dashboard
- `/live-data` - Real-time monitoring
- `/prediction` - Manual prediction
- `/chat` - AI chatbot
- `/trends` - Health analytics
- `/profile` - View profile
- `/profile/edit` - Edit profile
- `/download-report` - Download PDF report

**API Routes**
- `/api/predict` (POST) - Make health prediction
- `/api/sensor-data` (POST) - Receive sensor data
- `/api/historical-data` (GET) - Get historical vitals
- `/api/chat` (POST) - Send message to chatbot
- `/api/alerts/acknowledge` (POST) - Acknowledge alerts
- `/api/profile/update` (POST) - Update user profile

**Prediction Response Example**
```json
{
  "condition": "Low Risk",
  "confidence": 85,
  "risk_level": "Low",
  "recommendations": ["❤️ Heart rate is normal", "💨 Oxygen level is normal", "🌡️ Temperature is normal"],
  "risk_score": 0
}
```

---

## Machine Learning Model

**Model Details**
- Algorithm: Gradient Boosting Classifier
- Training Data: 200,020 patient records
- Features: 8 vital parameters (heart rate, respiratory rate, temperature, SpO₂, blood pressure, age, gender)
- Target: Cardiovascular Risk (Low Risk / High Risk)

**Risk Multiplier Factors**
- Medical conditions: hypertension, diabetes, heart disease, asthma, kidney disease, thyroid, anemia, high cholesterol
- Severity levels: mild (1.1x), moderate (1.3x), severe (1.6x)
- Lifestyle factors: smoking (1.4x current, 1.2x past), alcohol (1.3x regular, 1.1x occasional), exercise (1.2x sedentary, 1.05x light)

---

## Future Enhancements

**Environmental Sensors Integration**
- MQ135 for air quality monitoring (CO₂, CO, pollutants)
- DHT11 for ambient temperature and humidity
- Sound sensor for noise level monitoring
- PIR sensor for motion detection and activity tracking

**Planned Features**
- Mobile app for iOS and Android
- Telemedicine integration for doctor consultations
- Wearable device support (Apple Watch, Fitbit)
- Multi-language support for international deployment
- Cloud deployment on AWS/Azure
- HIPAA compliance for medical data security

**Model Improvements**
- Deep learning models (LSTM) for time-series prediction
- Federated learning for privacy-preserving training
- Real-time model updates from new data
- Multi-modal analysis combining vitals with medical images



## License

MIT License - see LICENSE file for details

Made with ❤️ for better healthcare accessibility
