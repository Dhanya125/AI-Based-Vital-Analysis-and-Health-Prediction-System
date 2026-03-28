# VitalHealth AI - Intelligent Health Monitoring & Prediction System
## 📋 Table of Contents

- [📖 Overview](#-overview)
- [✨ Key Features](#-key-features)
- [📊 Model Performance](#-model-performance)
- [🛠️ Technology Stack](#️-technology-stack)
- [📁 Project Structure](#-project-structure)
- [🚀 Installation & Setup](#-installation--setup)
- [🔌 Hardware Setup](#-hardware-setup)
- [🎯 Usage Guide](#-usage-guide)
- [📡 API Endpoints](#-api-endpoints)
- [🧠 Machine Learning Model](#-machine-learning-model)
- [🔒 Security Features](#-security-features)
- [📈 Future Enhancements](#-future-enhancements)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [👥 Authors](#-authors)

---

## 📖 Overview

**VitalHealth AI** is an innovative health monitoring and prediction platform that seamlessly integrates real-time sensor technology with advanced machine learning to deliver intelligent health risk assessments. The system utilizes three specialized biomedical sensors—**MAX30102** for heart rate and SpO₂ monitoring, **MLX90614** for non-contact temperature measurement, and **AD8232** for ECG signal acquisition—all interfaced through an ESP32 microcontroller that wirelessly transmits data to a sophisticated Flask-based web application. The heart of the system lies in its **Gradient Boosting Machine Learning model**, meticulously trained on over 200,000 patient records to achieve exceptional predictive accuracy of **94%** with an impressive **99.9% recall rate**, ensuring critical health risks are identified with minimal false negatives.

This project was developed for the **DevHub 1.0 Hackathon**, demonstrating the convergence of IoT, artificial intelligence, and healthcare to create an accessible, intelligent health monitoring solution.

---

## ✨ Key Features

### 🏥 Real-time Sensor Integration
- **MAX30102** - Heart Rate & SpO₂ monitoring via photoplethysmography
- **MLX90614** - Non-contact infrared temperature sensing
- **AD8232** - ECG signal acquisition with lead-off detection
- **ESP32** - Wireless data transmission to web application

### 📈 Live Visualization
- Real-time ECG waveform display using Chart.js
- Dynamic vital signs dashboard with color-coded status indicators
- Automatic updates every 3-5 seconds

### 💬 Intelligent Chatbot
- Natural language processing for health queries
- Stress management techniques and breathing exercises
- Sleep improvement recommendations
- Heart health and blood pressure guidance
- Personalized health summary generation

### 📊 Health Analytics
- Heart rate, SpO₂, and temperature trend charts
- Risk distribution pie chart
- Summary statistics with min, max, and average values
- Personalized health insights based on data patterns

### 📄 Professional Reports
- One-click PDF report generation
- Complete health summary with all vital signs
- Medical conditions and lifestyle profile
- Recent predictions and recommendations
- Suitable for medical consultations

### 🔐 User Management
- Secure registration with comprehensive health profile
- Medical conditions with severity levels (mild/moderate/severe)
- Lifestyle factor tracking (smoking, alcohol, exercise)
- BMI calculation with category classification
- Profile editing and updates

### ⚡ Real-time Alerts
- Critical value detection with immediate notifications
- Warning alerts for borderline readings
- Acknowledgment system for alert management
- Color-coded status badges (Normal/Warning/Critical)
---

## 🛠️ Technology Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.11+ | Core programming language |
| Flask | 2.3.3 | Web framework |
| SQLAlchemy | 3.1.1 | ORM for database operations |
| Flask-Login | 0.6.2 | User session management |
| bcrypt | 4.0.1 | Password hashing |
| SQLite | - | Lightweight database |

### Machine Learning
| Technology | Version | Purpose |
|------------|---------|---------|
| scikit-learn | 1.3.0 | Model training & evaluation |
| XGBoost | 1.7.6 | Gradient boosting implementation |
| Pandas | 2.0.3 | Data processing |
| NumPy | 1.24.3 | Numerical operations |
| Joblib | 1.3.2 | Model persistence |

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| Bootstrap | 5.3.0 | Responsive UI framework |
| Chart.js | 4.4.0 | ECG waveform visualization |
| Plotly | 5.17.0 | Health trend charts |
| Font Awesome | 6.4.0 | Icons and visual elements |
| Jinja2 | 3.1.2 | Template engine |

### Hardware
| Component | Purpose |
|-----------|---------|
| ESP32 | Microcontroller for sensor data acquisition |
| MAX30102 | Heart rate & SpO₂ monitoring |
| MLX90614 | Non-contact temperature sensing |
| AD8232 | ECG signal acquisition |

---
