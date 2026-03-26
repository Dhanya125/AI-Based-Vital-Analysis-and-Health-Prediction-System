import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///vital_health.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'app/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # ML Model paths - Update these with your actual model file locations
    MODEL_PATH = 'models/'  # Directory containing your model files
    GRADIENT_BOOSTING_MODEL = 'models/gradient_boosting_model.pkl'
    SCALER_PATH = 'models/scaler_gb.pkl'
    LABEL_ENCODER_PATH = 'models/label_encoder_gb.pkl'
    GENDER_ENCODER_PATH = 'models/gender_encoder_gb.pkl'
    FEATURE_NAMES_PATH = 'models/feature_names_gb.pkl'
    
    # Serial port for ESP32 (change based on your system)
    ESP32_PORT = 'COM3'  # Windows: 'COM3', Linux/Mac: '/dev/ttyUSB0'
    ESP32_BAUD = 115200