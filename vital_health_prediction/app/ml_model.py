import joblib
import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

class HealthPredictor:
    """
    Health Prediction System using Gradient Boosting Classifier
    Adapted for 3 sensors: Heart Rate, SpO2, Temperature
    """
    
    def __init__(self, model_path=None):
        self.model = None
        self.scaler = None
        self.label_encoder = None
        self.gender_encoder = None
        self.feature_names = None
        
        # Features available from your 3 sensors
        self.sensor_features = ['heart_rate', 'spo2', 'temperature']
        
        # Full features if model requires them (with defaults for missing ones)
        self.full_features = [
            'Heart Rate', 'Respiratory Rate', 'Body Temperature',
            'Oxygen Saturation', 'Systolic Blood Pressure',
            'Diastolic Blood Pressure', 'Age', 'Gender'
        ]
        
        # Conditions
        self.conditions = ['Low Risk', 'High Risk']
        
        # Load model if available
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
    
    def load_model(self, model_path):
        """Load pre-trained model and preprocessing objects"""
        try:
            # Load main model
            model_file = os.path.join(model_path, 'gradient_boosting_model.pkl')
            if os.path.exists(model_file):
                self.model = joblib.load(model_file)
                print(f"✓ Model loaded from {model_file}")
            
            # Load scaler
            scaler_file = os.path.join(model_path, 'scaler_gb.pkl')
            if os.path.exists(scaler_file):
                self.scaler = joblib.load(scaler_file)
                print(f"✓ Scaler loaded")
            
            # Load label encoder
            encoder_file = os.path.join(model_path, 'label_encoder_gb.pkl')
            if os.path.exists(encoder_file):
                self.label_encoder = joblib.load(encoder_file)
                print(f"✓ Label encoder loaded")
            
            # Load gender encoder
            gender_file = os.path.join(model_path, 'gender_encoder_gb.pkl')
            if os.path.exists(gender_file):
                self.gender_encoder = joblib.load(gender_file)
                print(f"✓ Gender encoder loaded")
            
            # Load feature names
            features_file = os.path.join(model_path, 'feature_names_gb.pkl')
            if os.path.exists(features_file):
                self.feature_names = joblib.load(features_file)
                print(f"✓ Feature names loaded")
            
            return True
            
        except Exception as e:
            print(f"⚠️ Error loading model: {e}")
            print("Falling back to rule-based prediction")
            return False
    
    def predict(self, heart_rate, spo2, temperature, 
                age=35, gender='Male', respiratory_rate=16, 
                systolic_bp=120, diastolic_bp=80):
        """
        Predict cardiovascular risk based on available vitals
        
        Parameters:
        -----------
        heart_rate : float - from MAX30102
        spo2 : float - from MAX30102  
        temperature : float - from MLX90614
        age : int - from user profile (default 35)
        gender : str - from user profile (default 'Male')
        respiratory_rate : float - estimated or default
        systolic_bp : float - estimated or default
        diastolic_bp : float - estimated or default
        """
        
        # If model is loaded, use it with all features
        if self.model is not None and self.scaler is not None:
            try:
                # Prepare full feature set
                input_data = {
                    'Heart Rate': heart_rate,
                    'Respiratory Rate': respiratory_rate,
                    'Body Temperature': temperature,
                    'Oxygen Saturation': spo2,
                    'Systolic Blood Pressure': systolic_bp,
                    'Diastolic Blood Pressure': diastolic_bp,
                    'Age': age,
                    'Gender': gender
                }
                
                input_df = pd.DataFrame([input_data])
                
                # Encode gender
                if self.gender_encoder is not None:
                    input_df['Gender'] = self.gender_encoder.transform(input_df['Gender'])
                else:
                    input_df['Gender'] = 1 if gender.lower() == 'male' else 0
                
                # Ensure correct feature order
                if self.feature_names is not None:
                    input_df = input_df[self.feature_names]
                
                # Scale features
                input_scaled = self.scaler.transform(input_df)
                
                # Predict
                prediction = self.model.predict(input_scaled)[0]
                probabilities = self.model.predict_proba(input_scaled)[0]
                
                # Get predicted class
                if self.label_encoder is not None:
                    predicted_class = self.label_encoder.inverse_transform([prediction])[0]
                else:
                    predicted_class = 'High Risk' if prediction == 1 else 'Low Risk'
                
                confidence = probabilities[prediction] * 100
                
                return {
                    'condition': predicted_class,
                    'confidence': round(confidence, 2),
                    'risk_level': self._get_risk_level(confidence),
                    'probabilities': {
                        'Low Risk': probabilities[0] * 100,
                        'High Risk': probabilities[1] * 100
                    },
                    'recommendations': self._generate_recommendations(
                        predicted_class, heart_rate, spo2, temperature, age
                    ),
                    'risk_factors': self._identify_risk_factors(
                        heart_rate, spo2, temperature, age
                    ),
                    'vitals_used': {
                        'heart_rate': heart_rate,
                        'spo2': spo2,
                        'temperature': temperature,
                        'age': age,
                        'gender': gender
                    }
                }
                
            except Exception as e:
                print(f"Model prediction error: {e}")
                # Fallback to rule-based
                return self._rule_based_prediction(
                    heart_rate, spo2, temperature, age, gender
                )
        
        # Use rule-based prediction
        return self._rule_based_prediction(
            heart_rate, spo2, temperature, age, gender
        )
    
    def _rule_based_prediction(self, heart_rate, spo2, temperature, age, gender):
        """Fallback prediction using medical guidelines (based on your 3 sensors)"""
        risk_score = 0
        risk_factors = []
        
        # Heart Rate Analysis (from MAX30102)
        if heart_rate > 100:
            risk_score += 2
            risk_factors.append(f"Tachycardia: {heart_rate} BPM")
        elif heart_rate < 60:
            risk_score += 1
            risk_factors.append(f"Bradycardia: {heart_rate} BPM")
        elif 60 <= heart_rate <= 100:
            risk_factors.append(f"Normal heart rate: {heart_rate} BPM")
        
        # SpO2 Analysis (from MAX30102)
        if spo2 < 95:
            risk_score += 2
            risk_factors.append(f"Hypoxia: {spo2}% SpO2")
        elif spo2 < 90:
            risk_score += 3
            risk_factors.append(f"Severe hypoxia: {spo2}% SpO2")
        else:
            risk_factors.append(f"Normal oxygen saturation: {spo2}%")
        
        # Temperature Analysis (from MLX90614)
        if temperature > 37.5:
            risk_score += 1
            risk_factors.append(f"Fever: {temperature}°C")
        elif temperature < 35.5:
            risk_score += 1
            risk_factors.append(f"Hypothermia: {temperature}°C")
        else:
            risk_factors.append(f"Normal temperature: {temperature}°C")
        
        # Age Factor
        if age > 65:
            risk_score += 1
            risk_factors.append(f"Elderly: {age} years")
        elif age < 1:
            risk_score += 1
            risk_factors.append(f"Infant: {age} years")
        
        # Combined risk indicators
        if heart_rate > 100 and temperature > 37.5:
            risk_score += 1
            risk_factors.append("Fever with tachycardia - possible infection")
        
        if heart_rate > 100 and spo2 < 95:
            risk_score += 1
            risk_factors.append("Tachycardia with hypoxia - respiratory distress")
        
        # Determine risk category
        if risk_score >= 4:
            predicted_class = "High Risk"
            confidence = min(70 + risk_score * 5, 95)
        elif risk_score >= 2:
            predicted_class = "High Risk"
            confidence = 50 + risk_score * 5
        else:
            predicted_class = "Low Risk"
            confidence = 85 - risk_score * 5
        
        confidence = min(max(confidence, 50), 95)
        
        return {
            'condition': predicted_class,
            'confidence': round(confidence, 2),
            'risk_level': self._get_risk_level(confidence),
            'probabilities': {
                'Low Risk': 100 - confidence if predicted_class == 'High Risk' else confidence,
                'High Risk': confidence if predicted_class == 'High Risk' else 100 - confidence
            },
            'recommendations': self._generate_recommendations(
                predicted_class, heart_rate, spo2, temperature, age
            ),
            'risk_factors': risk_factors,
            'vitals_used': {
                'heart_rate': heart_rate,
                'spo2': spo2,
                'temperature': temperature,
                'age': age,
                'gender': gender
            }
        }
    
    def _get_risk_level(self, confidence):
        """Determine risk level based on confidence"""
        if confidence >= 70:
            return "High"
        elif confidence >= 40:
            return "Moderate"
        else:
            return "Low"
    
    def _identify_risk_factors(self, heart_rate, spo2, temperature, age):
        """Identify specific risk factors from vitals"""
        risk_factors = []
        
        if heart_rate > 100:
            risk_factors.append(f"Tachycardia: {heart_rate} BPM")
        elif heart_rate < 60:
            risk_factors.append(f"Bradycardia: {heart_rate} BPM")
        
        if spo2 < 95:
            risk_factors.append(f"Low oxygen saturation: {spo2}%")
        
        if temperature > 37.5:
            risk_factors.append(f"Fever: {temperature}°C")
        elif temperature < 35.5:
            risk_factors.append(f"Hypothermia: {temperature}°C")
        
        if age > 65:
            risk_factors.append(f"Elderly: {age} years")
        
        return risk_factors
    
    def _generate_recommendations(self, risk_category, heart_rate, spo2, temperature, age):
        """Generate personalized health recommendations"""
        recommendations = []
        
        if risk_category == "High Risk":
            recommendations.append("⚠️ **URGENT:** Please consult a healthcare provider immediately")
            recommendations.append("📋 Monitor your vitals every 2 hours")
            recommendations.append("🏥 Seek emergency care if you experience chest pain, severe headache, or difficulty breathing")
        else:
            recommendations.append("✅ Continue regular health monitoring")
            recommendations.append("🏃 Maintain a healthy lifestyle with regular exercise")
            recommendations.append("🥗 Follow a balanced diet rich in fruits, vegetables, and whole grains")
        
        # Heart Rate recommendations
        if heart_rate > 100:
            recommendations.append("💓 Practice deep breathing exercises to lower heart rate")
            recommendations.append("☕ Reduce caffeine and alcohol intake")
            recommendations.append("🧘 Try relaxation techniques like meditation")
        elif heart_rate < 60 and not (age > 65 and heart_rate > 50):
            recommendations.append("💓 Consider light physical activity to improve cardiovascular health")
            recommendations.append("🏃 Start with walking 30 minutes daily")
        
        # SpO2 recommendations
        if spo2 < 95:
            recommendations.append("🌬️ Practice deep breathing exercises (inhale 4 sec, hold 4 sec, exhale 6 sec)")
            recommendations.append("💨 Ensure good ventilation in your room")
            recommendations.append("🏥 Seek medical attention if oxygen saturation drops below 92%")
        
        # Temperature recommendations
        if temperature > 37.5:
            recommendations.append("🌡️ Stay hydrated - drink plenty of water")
            recommendations.append("🛌 Rest and avoid strenuous activities")
            recommendations.append("💊 Take antipyretics if fever persists (consult doctor)")
        elif temperature < 35.5:
            recommendations.append("🧥 Keep warm with blankets and warm clothing")
            recommendations.append("☕ Drink warm fluids")
            recommendations.append("🏥 Seek medical attention if temperature doesn't normalize")
        
        # Age-based recommendations
        if age > 65:
            recommendations.append("👴 Regular check-ups recommended every 6 months")
            recommendations.append("💊 Review medications with your healthcare provider")
        elif age < 5:
            recommendations.append("👶 Ensure proper nutrition and hydration")
            recommendations.append("👨‍👩‍👧 Monitor for any signs of distress")
        
        # Remove duplicates
        recommendations = list(dict.fromkeys(recommendations))
        
        return recommendations
    
    def predict_from_sensors(self, heart_rate, spo2, temperature, age=35, gender='Male'):
        """Convenience method for 3-sensor prediction"""
        return self.predict(heart_rate, spo2, temperature, age, gender)
    
    def get_model_info(self):
        """Get information about the model"""
        info = {
            'model_type': 'Gradient Boosting Classifier (with rule-based fallback)',
            'sensors_used': ['MAX30102 (HR/SpO2)', 'MLX90614 (Temp)', 'AD8232 (ECG)'],
            'features_used': self.sensor_features,
            'conditions': self.conditions,
            'model_loaded': self.model is not None
        }
        
        if self.model is not None and hasattr(self.model, 'feature_importances_'):
            info['feature_importance'] = {
                'heart_rate': float(self.model.feature_importances_[0]) if len(self.model.feature_importances_) > 0 else 0,
                'spo2': float(self.model.feature_importances_[1]) if len(self.model.feature_importances_) > 1 else 0,
                'temperature': float(self.model.feature_importances_[2]) if len(self.model.feature_importances_) > 2 else 0
            }
        
        return info

# Initialize global predictor
predictor = HealthPredictor('models/')