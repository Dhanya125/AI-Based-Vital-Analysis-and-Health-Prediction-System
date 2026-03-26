"""
Utility functions for VitalHealth AI Application
"""

import os
import json
import hashlib
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from functools import wraps
from flask import jsonify, request, current_app

def calculate_age(birth_date):
    """Calculate age from birth date"""
    if not birth_date:
        return None
    today = datetime.now().date()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

def format_timestamp(dt):
    """Format datetime for display"""
    if not dt:
        return ""
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def validate_vital_limits(heart_rate, spo2, temperature):
    """Validate vital signs are within acceptable ranges"""
    errors = []
    
    if heart_rate:
        if heart_rate < 30 or heart_rate > 250:
            errors.append(f"Heart rate {heart_rate} BPM is outside normal range (30-250)")
    
    if spo2:
        if spo2 < 50 or spo2 > 100:
            errors.append(f"SpO2 {spo2}% is outside normal range (50-100)")
    
    if temperature:
        if temperature < 30 or temperature > 45:
            errors.append(f"Temperature {temperature}°C is outside normal range (30-45)")
    
    return errors

def calculate_risk_score(heart_rate, spo2, temperature, age):
    """
    Calculate a simple risk score based on vital signs
    Returns score from 0-100 (higher = higher risk)
    """
    score = 0
    
    # Heart Rate contribution
    if heart_rate:
        if heart_rate > 100:
            score += min((heart_rate - 100) * 0.5, 30)
        elif heart_rate < 60:
            score += min((60 - heart_rate) * 0.5, 20)
    
    # SpO2 contribution
    if spo2:
        if spo2 < 95:
            score += min((95 - spo2) * 2, 40)
    
    # Temperature contribution
    if temperature:
        if temperature > 37.5:
            score += min((temperature - 37.5) * 10, 30)
        elif temperature < 35.5:
            score += min((35.5 - temperature) * 5, 20)
    
    # Age contribution
    if age:
        if age > 65:
            score += 15
        elif age > 50:
            score += 10
        elif age > 40:
            score += 5
    
    return min(score, 100)

def get_risk_level(score):
    """Convert risk score to risk level"""
    if score >= 70:
        return "High"
    elif score >= 40:
        return "Moderate"
    else:
        return "Low"

def serialize_model_prediction(prediction):
    """Convert model prediction dictionary to JSON serializable format"""
    result = {
        'condition': prediction.get('condition', 'Unknown'),
        'confidence': float(prediction.get('confidence', 0)),
        'risk_level': prediction.get('risk_level', 'Low'),
        'recommendations': prediction.get('recommendations', []),
        'risk_factors': prediction.get('risk_factors', [])
    }
    
    if 'probabilities' in prediction:
        result['probabilities'] = {
            k: float(v) for k, v in prediction['probabilities'].items()
        }
    
    if 'vitals_used' in prediction:
        result['vitals_used'] = {
            k: float(v) if isinstance(v, (int, float)) else v 
            for k, v in prediction['vitals_used'].items()
        }
    
    return result

def generate_pdf_report(user, predictions, vitals):
    """
    Generate a PDF health report (placeholder - actual implementation would use reportlab or similar)
    """
    # This is a placeholder for PDF generation
    # In production, use reportlab or weasyprint
    return {
        'user': user.username,
        'email': user.email,
        'generated_at': datetime.now().isoformat(),
        'total_predictions': len(predictions),
        'total_vitals': len(vitals),
        'summary': {
            'avg_heart_rate': np.mean([v.heart_rate for v in vitals if v.heart_rate]) if vitals else None,
            'avg_spo2': np.mean([v.spo2 for v in vitals if v.spo2]) if vitals else None,
            'avg_temperature': np.mean([v.temperature for v in vitals if v.temperature]) if vitals else None
        }
    }

def load_model_artifacts(model_dir):
    """Load all model artifacts from directory"""
    artifacts = {
        'model': None,
        'scaler': None,
        'label_encoder': None,
        'gender_encoder': None,
        'feature_names': None
    }
    
    try:
        import joblib
        
        model_path = os.path.join(model_dir, 'gradient_boosting_model.pkl')
        if os.path.exists(model_path):
            artifacts['model'] = joblib.load(model_path)
        
        scaler_path = os.path.join(model_dir, 'scaler_gb.pkl')
        if os.path.exists(scaler_path):
            artifacts['scaler'] = joblib.load(scaler_path)
        
        encoder_path = os.path.join(model_dir, 'label_encoder_gb.pkl')
        if os.path.exists(encoder_path):
            artifacts['label_encoder'] = joblib.load(encoder_path)
        
        gender_path = os.path.join(model_dir, 'gender_encoder_gb.pkl')
        if os.path.exists(gender_path):
            artifacts['gender_encoder'] = joblib.load(gender_path)
        
        features_path = os.path.join(model_dir, 'feature_names_gb.pkl')
        if os.path.exists(features_path):
            artifacts['feature_names'] = joblib.load(features_path)
            
    except Exception as e:
        print(f"Error loading model artifacts: {e}")
    
    return artifacts

def save_uploaded_file(file, user_id, prediction_id):
    """Save uploaded file with secure filename"""
    import uuid
    
    # Get file extension
    ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
    
    # Create secure filename
    filename = f"{user_id}_{prediction_id}_{uuid.uuid4().hex[:8]}.{ext}"
    
    # Ensure upload directory exists
    upload_dir = os.path.join('app', 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    
    # Save file
    filepath = os.path.join(upload_dir, filename)
    file.save(filepath)
    
    return filename

def calculate_trend(current, previous):
    """Calculate trend between two values"""
    if not previous:
        return 'stable', 0
    
    diff = current - previous
    percent = (diff / previous) * 100 if previous != 0 else 0
    
    if diff > 0:
        trend = 'up'
    elif diff < 0:
        trend = 'down'
    else:
        trend = 'stable'
    
    return trend, abs(percent)

def format_vital_with_trend(current, previous):
    """Format vital sign with trend indicator"""
    trend, percent = calculate_trend(current, previous)
    
    if trend == 'up':
        icon = '▲'
        color = 'text-danger'
    elif trend == 'down':
        icon = '▼'
        color = 'text-success'
    else:
        icon = '●'
        color = 'text-muted'
    
    return f"{current} {icon} ({percent:.1f}%)", color