from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import bcrypt
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Demographic Details
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    
    # Lifestyle Factors
    smoker = db.Column(db.String(20))
    alcohol_consumer = db.Column(db.String(20))
    exercise_frequency = db.Column(db.String(20))
    
    # Medical Conditions
    medical_conditions = db.Column(db.Text)
    
    # Relationships
    vital_records = db.relationship('VitalRecord', backref='user', lazy=True)
    predictions = db.relationship('Prediction', backref='user', lazy=True)
    alerts = db.relationship('Alert', backref='user', lazy=True)
    chat_history = db.relationship('ChatMessage', backref='user', lazy=True)
    medical_reports = db.relationship('MedicalReport', backref='user', lazy=True)
    
    def set_password(self, password):
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def get_bmi(self):
        if self.height and self.weight:
            height_m = self.height / 100
            return round(self.weight / (height_m * height_m), 1)
        return None
    
    def get_bmi_category(self):
        bmi = self.get_bmi()
        if bmi:
            if bmi < 18.5:
                return "Underweight", "#3B82F6", "fa-seedling"
            elif bmi < 25:
                return "Normal", "#10B981", "fa-smile"
            elif bmi < 30:
                return "Overweight", "#F59E0B", "fa-chart-line"
            else:
                return "Obese", "#EF4444", "fa-exclamation-triangle"
        return "Unknown", "#6B7280", "fa-question"
    
    def get_medical_conditions_dict(self):
        if self.medical_conditions:
            return json.loads(self.medical_conditions)
        return {
            'hypertension': {'enabled': False, 'severity': 'mild'},
            'diabetes': {'enabled': False, 'severity': 'mild'},
            'heart_disease': {'enabled': False, 'severity': 'mild'},
            'asthma': {'enabled': False, 'severity': 'mild'},
            'kidney_disease': {'enabled': False, 'severity': 'mild'},
            'thyroid': {'enabled': False, 'severity': 'mild'},
            'anemia': {'enabled': False, 'severity': 'mild'},
            'high_cholesterol': {'enabled': False, 'severity': 'mild'}
        }
    

class VitalRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    heart_rate = db.Column(db.Float)
    spo2 = db.Column(db.Float)
    temperature = db.Column(db.Float)
    ecg_signal = db.Column(db.Text)

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    vital_record_id = db.Column(db.Integer, db.ForeignKey('vital_record.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    predicted_condition = db.Column(db.String(100))
    confidence_score = db.Column(db.Float)
    risk_level = db.Column(db.String(20))
    recommendations = db.Column(db.Text)

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    alert_type = db.Column(db.String(50))
    message = db.Column(db.Text)
    acknowledged = db.Column(db.Boolean, default=False)

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_message = db.Column(db.Text)
    bot_response = db.Column(db.Text)

class MedicalReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    prediction_id = db.Column(db.Integer, db.ForeignKey('prediction.id'))
    report_file = db.Column(db.String(200))
    doctor_diagnosis = db.Column(db.String(200))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    verified = db.Column(db.Boolean, default=False)