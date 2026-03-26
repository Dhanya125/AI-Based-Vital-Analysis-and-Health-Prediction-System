# from flask import render_template, request, jsonify, redirect, url_for, flash, send_file
# from flask_login import login_user, logout_user, login_required, current_user
# from app import db
# from app.models import User, VitalRecord, Prediction, Alert, ChatMessage
# import json
# from datetime import datetime
# from flask import Blueprint
# import io
# from reportlab.lib import colors
# from reportlab.lib.pagesizes import A4
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.units import inch
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
# from reportlab.lib.enums import TA_CENTER, TA_LEFT

# # ==================== BLUEPRINT DEFINITIONS ====================
# main_bp = Blueprint('main', __name__)
# auth_bp = Blueprint('auth', __name__)
# api_bp = Blueprint('api', __name__)


# # ==================== PDF REPORT GENERATION ====================

# def generate_health_report(user, vitals_data, predictions_data):
#     """Generate a beautiful PDF health report"""
    
#     buffer = io.BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    
#     COLOR_PRIMARY = colors.HexColor('#9B7BB5')
#     COLOR_BG_LIGHT = colors.HexColor('#FCF9F5')
#     COLOR_BG_HEADER = colors.HexColor('#E9E2F5')
#     COLOR_BORDER = colors.HexColor('#E5D9CC')
#     COLOR_TEXT = colors.HexColor('#4A4A6A')
    
#     styles = getSampleStyleSheet()
    
#     title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontName='Helvetica-Bold',
#                                   fontSize=24, textColor=COLOR_PRIMARY, alignment=TA_CENTER, spaceAfter=30)
#     section_style = ParagraphStyle('SectionHeader', parent=styles['Heading2'], fontName='Helvetica-Bold',
#                                     fontSize=14, textColor=COLOR_PRIMARY, spaceBefore=20, spaceAfter=12)
#     normal_style = ParagraphStyle('CustomNormal', parent=styles['Normal'], fontName='Helvetica',
#                                    fontSize=10, textColor=COLOR_TEXT, spaceAfter=6)
    
#     story = []
    
#     story.append(Paragraph("VitalHealth AI", title_style))
#     story.append(Paragraph(f"Report for {user.username}", normal_style))
#     story.append(Spacer(1, 20))
    
#     # Patient Information
#     story.append(Paragraph("Patient Information", section_style))
#     bmi = user.get_bmi()
#     patient_info = [
#         ["Name:", user.username], ["Email:", user.email],
#         ["Age:", f"{user.age}" if user.age else "Not set"],
#         ["Gender:", user.gender if user.gender else "Not set"],
#         ["BMI:", f"{bmi}" if bmi else "Not calculated"],
#         ["Date:", datetime.now().strftime('%B %d, %Y')],
#     ]
#     patient_table = Table(patient_info, colWidths=[2*inch, 3*inch])
#     patient_table.setStyle(TableStyle([
#         ('BACKGROUND', (0, 0), (-1, -1), COLOR_BG_LIGHT),
#         ('BOX', (0, 0), (-1, -1), 1, COLOR_BORDER),
#     ]))
#     story.append(patient_table)
#     story.append(Spacer(1, 15))
    
#     # Vital Signs
#     if vitals_data:
#         story.append(Paragraph("Recent Vital Signs", section_style))
#         data = [["Date/Time", "Heart Rate", "SpO₂", "Temperature"]]
#         for v in vitals_data[:10]:
#             data.append([
#                 v.timestamp.strftime('%Y-%m-%d %H:%M'),
#                 f"{v.heart_rate} BPM" if v.heart_rate else "-",
#                 f"{v.spo2}%" if v.spo2 else "-",
#                 f"{v.temperature}°C" if v.temperature else "-"
#             ])
#         table = Table(data, colWidths=[2*inch, 1.3*inch, 1.3*inch, 1.3*inch])
#         table.setStyle(TableStyle([
#             ('BACKGROUND', (0, 0), (-1, 0), COLOR_BG_HEADER),
#             ('GRID', (0, 0), (-1, -1), 1, COLOR_BORDER),
#         ]))
#         story.append(table)
#         story.append(Spacer(1, 15))
    
#     # Predictions
#     if predictions_data:
#         story.append(Paragraph("Health Assessments", section_style))
#         data = [["Date/Time", "Prediction", "Confidence", "Risk"]]
#         for p in predictions_data[:5]:
#             data.append([
#                 p.timestamp.strftime('%Y-%m-%d %H:%M'),
#                 p.predicted_condition,
#                 f"{p.confidence_score}%",
#                 p.risk_level
#             ])
#         table = Table(data, colWidths=[1.8*inch, 1.5*inch, 1.2*inch, 1.2*inch])
#         table.setStyle(TableStyle([
#             ('BACKGROUND', (0, 0), (-1, 0), COLOR_BG_HEADER),
#             ('GRID', (0, 0), (-1, -1), 1, COLOR_BORDER),
#         ]))
#         story.append(table)
    
#     doc.build(story)
#     buffer.seek(0)
#     return buffer


# # ==================== AUTHENTICATION ROUTES ====================

# @auth_bp.route('/register', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.dashboard'))
    
#     if request.method == 'POST':
#         username = request.form.get('username')
#         email = request.form.get('email')
#         password = request.form.get('password')
        
#         if User.query.filter_by(username=username).first():
#             flash('Username already exists', 'danger')
#             return redirect(url_for('auth.register'))
        
#         if User.query.filter_by(email=email).first():
#             flash('Email already registered', 'danger')
#             return redirect(url_for('auth.register'))
        
#         medical_conditions = {}
#         condition_list = ['hypertension', 'diabetes', 'heart_disease', 'asthma', 
#                          'kidney_disease', 'thyroid', 'anemia', 'high_cholesterol']
        
#         for condition in condition_list:
#             enabled = request.form.get(f'condition_{condition}') == 'on'
#             severity = request.form.get(f'severity_{condition}', 'mild')
#             medical_conditions[condition] = {'enabled': enabled, 'severity': severity}
        
#         user = User(
#             username=username,
#             email=email,
#             age=request.form.get('age', type=int),
#             gender=request.form.get('gender'),
#             height=request.form.get('height', type=float),
#             weight=request.form.get('weight', type=float),
#             smoker=request.form.get('smoker'),
#             alcohol_consumer=request.form.get('alcohol'),
#             exercise_frequency=request.form.get('exercise'),
#             medical_conditions=json.dumps(medical_conditions)
#         )
#         user.set_password(password)
        
#         db.session.add(user)
#         db.session.commit()
        
#         flash('Registration successful!', 'success')
#         return redirect(url_for('auth.login'))
    
#     return render_template('register.html')

# @auth_bp.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.dashboard'))
    
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#         user = User.query.filter_by(username=username).first()
        
#         if user and user.check_password(password):
#             login_user(user)
#             return redirect(url_for('main.dashboard'))
#         else:
#             flash('Invalid credentials', 'danger')
    
#     return render_template('login.html')

# @auth_bp.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('auth.login'))


# # ==================== MAIN ROUTES ====================

# @main_bp.route('/')
# def index():
#     return render_template('index.html')

# @main_bp.route('/dashboard')
# @login_required
# def dashboard():
#     recent_vitals = VitalRecord.query.filter_by(user_id=current_user.id)\
#         .order_by(VitalRecord.timestamp.desc()).limit(10).all()
#     unread_alerts = Alert.query.filter_by(user_id=current_user.id, acknowledged=False).all()
    
#     return render_template('dashboard.html',
#                          recent_vitals=recent_vitals,
#                          unread_alerts=unread_alerts,
#                          now=datetime.now())

# @main_bp.route('/live-data')
# @login_required
# def live_data():
#     return render_template('live_data.html')

# @main_bp.route('/prediction')
# @login_required
# def prediction():
#     return render_template('prediction.html')

# @main_bp.route('/chat')
# @login_required
# def chat():
#     chat_history = ChatMessage.query.filter_by(user_id=current_user.id)\
#         .order_by(ChatMessage.timestamp.desc()).limit(50).all()
#     return render_template('chat.html', chat_history=chat_history)

# @main_bp.route('/profile')
# @login_required
# def profile_view():
#     return render_template('profile_view.html', user=current_user)

# @main_bp.route('/profile/edit')
# @login_required
# def profile_edit():
#     return render_template('profile_edit.html', user=current_user)

# @main_bp.route('/download-report')
# @login_required
# def download_report():
#     try:
#         vitals = VitalRecord.query.filter_by(user_id=current_user.id)\
#             .order_by(VitalRecord.timestamp.desc()).limit(30).all()
#         predictions = Prediction.query.filter_by(user_id=current_user.id)\
#             .order_by(Prediction.timestamp.desc()).limit(10).all()
        
#         pdf_buffer = generate_health_report(current_user, vitals, predictions)
        
#         return send_file(
#             pdf_buffer,
#             as_attachment=True,
#             download_name=f"VitalHealth_Report_{current_user.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
#             mimetype='application/pdf'
#         )
#     except Exception as e:
#         flash(f'Error: {str(e)}', 'danger')
#         return redirect(url_for('main.dashboard'))


# # ==================== API ROUTES ====================

# @api_bp.route('/chat', methods=['POST'])
# @login_required
# def chat_api():
#     data = request.get_json()
#     user_message = data.get('message', '')
    
#     msg = user_message.lower()
#     if any(w in msg for w in ['stress', 'anxious']):
#         response = "😌 Try 4-7-8 breathing: Inhale 4 sec, hold 7 sec, exhale 8 sec. Repeat 4 times."
#     elif any(w in msg for w in ['sleep', 'insomnia']):
#         response = "😴 Tips: Consistent schedule, no screens before bed, cool dark room."
#     elif any(w in msg for w in ['heart', 'palpitations']):
#         response = "❤️ Normal heart rate: 60-100 BPM. See doctor if concerned."
#     elif any(w in msg for w in ['bp', 'blood pressure']):
#         response = "🩸 Normal BP: <120/80. Exercise, low salt, limit alcohol."
#     elif any(w in msg for w in ['exercise', 'workout']):
#         response = "🏃 Aim for 150 min moderate exercise weekly. Start with daily walks."
#     elif any(w in msg for w in ['diet', 'food']):
#         response = "🥗 Eat vegetables, lean protein, whole grains. Drink 8 glasses water daily."
#     else:
#         response = "👋 I'm your AI Health Assistant! Ask about stress, sleep, heart, BP, exercise, or diet."
    
#     chat = ChatMessage(user_id=current_user.id, user_message=user_message, bot_response=response)
#     db.session.add(chat)
#     db.session.commit()
    
#     return jsonify({'response': response})

# @api_bp.route('/predict', methods=['POST'])
# @login_required
# def predict():
#     try:
#         data = request.get_json()
#         print(f"Received prediction data: {data}")
        
#         heart_rate = float(data.get('heart_rate'))
#         spo2 = float(data.get('spo2'))
#         temperature = float(data.get('temperature'))
        
#         # Calculate risk score
#         risk_score = 0
#         recommendations = []
        
#         if heart_rate > 100:
#             risk_score += 20
#             recommendations.append("❤️ Heart rate elevated - practice deep breathing")
#         elif heart_rate < 60:
#             risk_score += 10
#             recommendations.append("❤️ Heart rate lower than normal - monitor")
#         else:
#             recommendations.append("❤️ Heart rate is normal")
        
#         if spo2 < 90:
#             risk_score += 40
#             recommendations.append("💨 Critical low oxygen - seek medical help")
#         elif spo2 < 95:
#             risk_score += 25
#             recommendations.append("💨 Low oxygen - deep breathing exercises")
#         else:
#             recommendations.append("💨 Oxygen level is normal")
        
#         if temperature > 38.5:
#             risk_score += 30
#             recommendations.append("🌡️ High fever - rest and hydrate")
#         elif temperature > 37.5:
#             risk_score += 15
#             recommendations.append("🌡️ Mild fever - rest and hydrate")
#         elif temperature < 35.5:
#             risk_score += 15
#             recommendations.append("🌡️ Low temperature - keep warm")
#         else:
#             recommendations.append("🌡️ Temperature is normal")
        
#         if risk_score >= 60:
#             condition = "High Risk"
#             risk_level = "High"
#             confidence = 85
#         elif risk_score >= 30:
#             condition = "Moderate Risk"
#             risk_level = "Moderate"
#             confidence = 65
#         else:
#             condition = "Low Risk"
#             risk_level = "Low"
#             confidence = 85
        
#         # Save vital record
#         vital = VitalRecord(
#             user_id=current_user.id,
#             heart_rate=heart_rate,
#             spo2=spo2,
#             temperature=temperature
#         )
#         db.session.add(vital)
#         db.session.commit()
        
#         # Save prediction
#         pred = Prediction(
#             user_id=current_user.id,
#             vital_record_id=vital.id,
#             predicted_condition=condition,
#             confidence_score=confidence,
#             risk_level=risk_level,
#             recommendations=json.dumps(recommendations)
#         )
#         db.session.add(pred)
#         db.session.commit()
        
#         # Create alert for high risk
#         if risk_level == "High":
#             alert = Alert(
#                 user_id=current_user.id,
#                 alert_type="critical",
#                 message=f"High risk detected! HR:{heart_rate}, SpO2:{spo2}, Temp:{temperature}"
#             )
#             db.session.add(alert)
#             db.session.commit()
        
#         return jsonify({
#             'condition': condition,
#             'confidence': confidence,
#             'risk_level': risk_level,
#             'recommendations': recommendations,
#             'risk_score': risk_score
#         })
        
#     except Exception as e:
#         print(f"Prediction error: {str(e)}")
#         return jsonify({'error': str(e)}), 400

# @api_bp.route('/sensor-data', methods=['POST'])
# def sensor_data():
#     try:
#         data = request.get_json()
#         return jsonify({'status': 'success'})
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 400

# @api_bp.route('/historical-data')
# @login_required
# def historical_data():
#     vitals = VitalRecord.query.filter_by(user_id=current_user.id)\
#         .order_by(VitalRecord.timestamp.desc()).limit(50).all()
#     return jsonify([{
#         'timestamp': v.timestamp.isoformat(),
#         'heart_rate': v.heart_rate,
#         'spo2': v.spo2,
#         'temperature': v.temperature
#     } for v in vitals])

# @api_bp.route('/alerts/acknowledge', methods=['POST'])
# @login_required
# def acknowledge_alerts():
#     Alert.query.filter_by(user_id=current_user.id, acknowledged=False).update({'acknowledged': True})
#     db.session.commit()
#     return jsonify({'success': True})

# @api_bp.route('/alerts/acknowledge/<int:alert_id>', methods=['POST'])
# @login_required
# def acknowledge_single_alert(alert_id):
#     alert = Alert.query.get(alert_id)
#     if alert and alert.user_id == current_user.id:
#         alert.acknowledged = True
#         db.session.commit()
#         return jsonify({'success': True})
#     return jsonify({'success': False}), 404

# @api_bp.route('/profile/update', methods=['POST'])
# @login_required
# def update_profile():
#     current_user.age = request.form.get('age', type=int)
#     current_user.gender = request.form.get('gender')
#     current_user.height = request.form.get('height', type=float)
#     current_user.weight = request.form.get('weight', type=float)
#     current_user.smoker = request.form.get('smoker')
#     current_user.alcohol_consumer = request.form.get('alcohol')
#     current_user.exercise_frequency = request.form.get('exercise')
    
#     db.session.commit()
#     flash('Profile updated!', 'success')
#     return redirect(url_for('main.profile_view'))
# from app.graphs import (
#     create_heart_rate_chart, create_spo2_chart, create_temperature_chart,
#     create_risk_distribution_chart, create_summary_stats, generate_insights
# )
# # from app.graphs import (
# #     create_heart_rate_chart, create_spo2_chart, create_temperature_chart,
# #     create_risk_distribution_chart, create_vitals_comparison_chart,
# #     create_bmi_gauge, create_activity_summary
# # )
# from flask import render_template, request, jsonify, redirect, url_for, flash, send_file
# from flask_login import login_user, logout_user, login_required, current_user
# from app import db
# from app.models import User, VitalRecord, Prediction, Alert, ChatMessage
# import json
# from datetime import datetime
# from flask import Blueprint
# import io
# from reportlab.lib import colors
# from reportlab.lib.pagesizes import A4
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.units import inch
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
# from reportlab.lib.enums import TA_CENTER, TA_LEFT

# # ==================== BLUEPRINT DEFINITIONS ====================
# # THESE MUST BE AT THE TOP OF THE FILE
# main_bp = Blueprint('main', __name__)
# auth_bp = Blueprint('auth', __name__)
# api_bp = Blueprint('api', __name__)
from flask import render_template, request, jsonify, redirect, url_for, flash, send_file
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, VitalRecord, Prediction, Alert, ChatMessage
import json
from datetime import datetime
from flask import Blueprint
import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# Import only the functions you actually use in routes
# Remove create_vitals_comparison_chart from this list
from app.graphs import (
    create_heart_rate_chart, 
    create_spo2_chart, 
    create_temperature_chart,
    create_risk_distribution_chart,
    create_summary_stats, 
    generate_insights
)

# ==================== BLUEPRINT DEFINITIONS ====================
main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)
api_bp = Blueprint('api', __name__)

# ==================== PDF REPORT GENERATION ====================

def generate_health_report(user, vitals_data, predictions_data):
    """Generate a beautiful and COMPLETE PDF health report"""
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=72)
    
    # Colors
    COLOR_PRIMARY = colors.HexColor('#9B7BB5')
    COLOR_SECONDARY = colors.HexColor('#6FBF8C')
    COLOR_ACCENT = colors.HexColor('#E98585')
    COLOR_WARNING = colors.HexColor('#F5A97F')
    COLOR_TEXT = colors.HexColor('#4A4A6A')
    COLOR_TEXT_LIGHT = colors.HexColor('#8A8AA8')
    COLOR_BORDER = colors.HexColor('#E5D9CC')
    COLOR_BG_LIGHT = colors.HexColor('#FCF9F5')
    COLOR_BG_HEADER = colors.HexColor('#E9E2F5')
    
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        textColor=COLOR_PRIMARY,
        alignment=TA_CENTER,
        spaceAfter=30,
        spaceBefore=20
    )
    
    section_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor=COLOR_PRIMARY,
        spaceBefore=20,
        spaceAfter=12
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=COLOR_TEXT,
        spaceAfter=6,
        leading=14
    )
    
    small_style = ParagraphStyle(
        'SmallText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        textColor=COLOR_TEXT_LIGHT,
        spaceAfter=4
    )
    
    story = []
    
    # ==================== HEADER ====================
    story.append(Paragraph("VitalHealth AI", title_style))
    story.append(Paragraph("Comprehensive Health Assessment Report", small_style))
    story.append(Spacer(1, 20))
    
    # ==================== PATIENT INFORMATION ====================
    story.append(Paragraph("Patient Information", section_style))
    
    bmi = user.get_bmi()
    bmi_category = user.get_bmi_category()[0] if bmi else "Not calculated"
    
    patient_info = [
        ["Full Name:", user.username],
        ["Email Address:", user.email],
        ["Age:", f"{user.age} years" if user.age else "Not set"],
        ["Gender:", user.gender if user.gender else "Not set"],
        ["Height:", f"{user.height} cm" if user.height else "Not set"],
        ["Weight:", f"{user.weight} kg" if user.weight else "Not set"],
        ["BMI:", f"{bmi} ({bmi_category})" if bmi else "Not calculated"],
        ["Report Date:", datetime.now().strftime('%B %d, %Y at %H:%M')],
    ]
    
    patient_table = Table(patient_info, colWidths=[2.5*inch, 3.5*inch])
    patient_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), COLOR_TEXT),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_BG_LIGHT),
        ('BOX', (0, 0), (-1, -1), 1, COLOR_BORDER),
    ]))
    story.append(patient_table)
    story.append(Spacer(1, 15))
    
    # ==================== LIFESTYLE PROFILE ====================
    story.append(Paragraph("Lifestyle Profile", section_style))
    
    lifestyle_data = [
        ["Smoking Status:", user.smoker.replace('_', ' ').title() if user.smoker else "Not set"],
        ["Alcohol Consumption:", user.alcohol_consumer.replace('_', ' ').title() if user.alcohol_consumer else "Not set"],
        ["Exercise Frequency:", user.exercise_frequency.replace('_', ' ').title() if user.exercise_frequency else "Not set"],
    ]
    
    lifestyle_table = Table(lifestyle_data, colWidths=[2.5*inch, 3.5*inch])
    lifestyle_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(lifestyle_table)
    story.append(Spacer(1, 15))
    
    # ==================== MEDICAL CONDITIONS ====================
    story.append(Paragraph("Medical Conditions", section_style))
    
    conditions = user.get_medical_conditions_dict()
    active_conditions = [(c.replace('_', ' ').title(), data['severity'].title()) 
                         for c, data in conditions.items() if data.get('enabled')]
    
    if active_conditions:
        condition_data = [["Condition", "Severity", "Status"]] + \
                         [[name, severity, "Active"] for name, severity in active_conditions]
        
        condition_table = Table(condition_data, colWidths=[2.5*inch, 1.5*inch, 1.2*inch])
        condition_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (0, 0), (-1, 0), COLOR_BG_HEADER),
            ('TEXTCOLOR', (0, 0), (-1, 0), COLOR_PRIMARY),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, COLOR_BORDER),
            ('BACKGROUND', (0, 1), (-1, -1), COLOR_BG_LIGHT),
        ]))
        story.append(condition_table)
    else:
        story.append(Paragraph("No active medical conditions reported.", normal_style))
    story.append(Spacer(1, 15))
    
    # ==================== VITAL SIGNS SUMMARY ====================
    if vitals_data:
        story.append(Paragraph("Vital Signs Summary", section_style))
        
        # Calculate statistics
        hr_values = [v.heart_rate for v in vitals_data if v.heart_rate]
        spo2_values = [v.spo2 for v in vitals_data if v.spo2]
        temp_values = [v.temperature for v in vitals_data if v.temperature]
        
        avg_hr = sum(hr_values) / len(hr_values) if hr_values else 0
        avg_spo2 = sum(spo2_values) / len(spo2_values) if spo2_values else 0
        avg_temp = sum(temp_values) / len(temp_values) if temp_values else 0
        
        min_hr = min(hr_values) if hr_values else 0
        max_hr = max(hr_values) if hr_values else 0
        min_spo2 = min(spo2_values) if spo2_values else 0
        max_spo2 = max(spo2_values) if spo2_values else 0
        min_temp = min(temp_values) if temp_values else 0
        max_temp = max(temp_values) if temp_values else 0
        
        summary_data = [
            ["Metric", "Average", "Range", "Status", "Normal Range"],
            ["Heart Rate", f"{avg_hr:.0f} BPM", f"{min_hr:.0f}-{max_hr:.0f}", 
             "Normal" if 60 <= avg_hr <= 100 else "Alert", "60-100 BPM"],
            ["Oxygen Saturation", f"{avg_spo2:.0f}%", f"{min_spo2:.0f}-{max_spo2:.0f}",
             "Normal" if avg_spo2 >= 95 else "Alert", "95-100%"],
            ["Temperature", f"{avg_temp:.1f}°C", f"{min_temp:.1f}-{max_temp:.1f}",
             "Normal" if 36.1 <= avg_temp <= 37.2 else "Alert", "36.1-37.2°C"],
        ]
        
        summary_table = Table(summary_data, colWidths=[1.2*inch, 1.2*inch, 1.5*inch, 1*inch, 1.2*inch])
        summary_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BACKGROUND', (0, 0), (-1, 0), COLOR_BG_HEADER),
            ('TEXTCOLOR', (0, 0), (-1, 0), COLOR_PRIMARY),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, COLOR_BORDER),
            ('BACKGROUND', (0, 1), (-1, -1), COLOR_BG_LIGHT),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 15))
        
        # ==================== RECENT VITAL RECORDS ====================
        story.append(Paragraph("Recent Vital Records (Last 10)", section_style))
        
        recent_data = [["Date & Time", "Heart Rate (BPM)", "SpO₂ (%)", "Temperature (°C)"]]
        for v in vitals_data[:10]:
            recent_data.append([
                v.timestamp.strftime('%Y-%m-%d %H:%M'),
                f"{v.heart_rate:.0f}" if v.heart_rate else "-",
                f"{v.spo2:.0f}" if v.spo2 else "-",
                f"{v.temperature:.1f}" if v.temperature else "-"
            ])
        
        recent_table = Table(recent_data, colWidths=[1.8*inch, 1.2*inch, 1.2*inch, 1.2*inch])
        recent_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 0), (-1, 0), COLOR_BG_HEADER),
            ('TEXTCOLOR', (0, 0), (-1, 0), COLOR_PRIMARY),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
            ('BACKGROUND', (0, 1), (-1, -1), COLOR_BG_LIGHT),
        ]))
        story.append(recent_table)
        story.append(Spacer(1, 15))
    
    # ==================== HEALTH RISK ASSESSMENTS ====================
    if predictions_data:
        story.append(Paragraph("Health Risk Assessments", section_style))
        
        pred_data = [["Date/Time", "Prediction", "Confidence", "Risk Level"]]
        for p in predictions_data[:10]:
            pred_data.append([
                p.timestamp.strftime('%Y-%m-%d %H:%M'),
                p.predicted_condition,
                f"{p.confidence_score:.0f}%",
                p.risk_level
            ])
        
        pred_table = Table(pred_data, colWidths=[1.8*inch, 1.5*inch, 1.2*inch, 1.2*inch])
        pred_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BACKGROUND', (0, 0), (-1, 0), COLOR_BG_HEADER),
            ('TEXTCOLOR', (0, 0), (-1, 0), COLOR_PRIMARY),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, COLOR_BORDER),
            ('BACKGROUND', (0, 1), (-1, -1), COLOR_BG_LIGHT),
        ]))
        story.append(pred_table)
        story.append(Spacer(1, 15))
    
    # ==================== PERSONALIZED RECOMMENDATIONS ====================
    story.append(Paragraph("Personalized Health Recommendations", section_style))
    
    recommendations = []
    
    # BMI Recommendations
    if bmi:
        if bmi < 18.5:
            recommendations.append("📊 • Your BMI indicates underweight. Consider nutritional counseling.")
        elif bmi > 25:
            recommendations.append("📊 • Your BMI indicates overweight. Aim for gradual weight loss.")
        else:
            recommendations.append("📊 • Your BMI is healthy. Maintain with balanced nutrition.")
    
    # Heart Rate Recommendations
    if avg_hr > 100:
        recommendations.append("❤️ • Your average heart rate is elevated. Practice stress reduction.")
    elif avg_hr < 60 and avg_hr > 0:
        recommendations.append("❤️ • Your average heart rate is lower than normal. Monitor for dizziness.")
    
    # SpO2 Recommendations
    if avg_spo2 < 95:
        recommendations.append("💨 • Your oxygen levels are below optimal. Practice deep breathing exercises.")
    
    # Lifestyle Recommendations
    if user.smoker == 'current':
        recommendations.append("🚭 • Smoking cessation is the most important step for your health.")
    if user.alcohol_consumer == 'regular':
        recommendations.append("🍷 • Regular alcohol consumption increases health risks. Consider reducing.")
    if user.exercise_frequency == 'sedentary':
        recommendations.append("🏃 • Start with light physical activity: 10-minute walks daily.")
    
    if not recommendations:
        recommendations.append("✅ • You're doing great! Continue maintaining your healthy lifestyle.")
    
    recommendations.append("🏥 • Always consult healthcare professionals for medical advice.")
    
    for rec in recommendations:
        story.append(Paragraph(rec, normal_style))
        story.append(Spacer(1, 5))
    
    story.append(Spacer(1, 15))
    
    # ==================== FOOTER ====================
    story.append(Spacer(1, 20))
    story.append(Paragraph("-" * 70, small_style))
    story.append(Paragraph("Report generated by VitalHealth AI - Smart Health Monitoring System", small_style))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}", small_style))
    story.append(Paragraph("This report is for informational purposes only. Please consult a healthcare professional for medical advice.", 
                          ParagraphStyle('Footer', parent=small_style, textColor=COLOR_TEXT_LIGHT, alignment=TA_CENTER)))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer


# ==================== AUTHENTICATION ROUTES ====================

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('auth.register'))
        
        medical_conditions = {}
        condition_list = ['hypertension', 'diabetes', 'heart_disease', 'asthma', 
                         'kidney_disease', 'thyroid', 'anemia', 'high_cholesterol']
        
        for condition in condition_list:
            enabled = request.form.get(f'condition_{condition}') == 'on'
            severity = request.form.get(f'severity_{condition}', 'mild')
            medical_conditions[condition] = {'enabled': enabled, 'severity': severity}
        
        user = User(
            username=username,
            email=email,
            age=request.form.get('age', type=int),
            gender=request.form.get('gender'),
            height=request.form.get('height', type=float),
            weight=request.form.get('weight', type=float),
            smoker=request.form.get('smoker'),
            alcohol_consumer=request.form.get('alcohol'),
            exercise_frequency=request.form.get('exercise'),
            medical_conditions=json.dumps(medical_conditions)
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful!', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


# ==================== MAIN ROUTES ====================

@main_bp.route('/')
def index():
    return render_template('index.html')

# @main_bp.route('/dashboard')
# @login_required
# def dashboard():
#     recent_vitals = VitalRecord.query.filter_by(user_id=current_user.id)\
#         .order_by(VitalRecord.timestamp.desc()).limit(20).all()
#     recent_predictions = Prediction.query.filter_by(user_id=current_user.id)\
#         .order_by(Prediction.timestamp.desc()).limit(20).all()
#     unread_alerts = Alert.query.filter_by(user_id=current_user.id, acknowledged=False).all()
    
#     # Generate charts
#     hr_chart = create_heart_rate_chart(recent_vitals)
#     spo2_chart = create_spo2_chart(recent_vitals)
#     temp_chart = create_temperature_chart(recent_vitals)
#     risk_chart = create_risk_distribution_chart(recent_predictions)
#     vitals_comparison = create_vitals_comparison_chart(recent_vitals)
#     bmi_gauge = create_bmi_gauge(current_user.get_bmi())
#     activity_chart = create_activity_summary(current_user)
    
#     return render_template('dashboard.html',
#                          recent_vitals=recent_vitals,
#                          recent_predictions=recent_predictions,
#                          unread_alerts=unread_alerts,
#                          now=datetime.now(),
#                          hr_chart=hr_chart,
#                          spo2_chart=spo2_chart,
#                          temp_chart=temp_chart,
#                          risk_chart=risk_chart,
#                          vitals_comparison=vitals_comparison,
#                          bmi_gauge=bmi_gauge,
#                          activity_chart=activity_chart)
@main_bp.route('/dashboard')
@login_required
def dashboard():
    recent_vitals = VitalRecord.query.filter_by(user_id=current_user.id)\
        .order_by(VitalRecord.timestamp.desc()).limit(10).all()
    recent_predictions = Prediction.query.filter_by(user_id=current_user.id)\
        .order_by(Prediction.timestamp.desc()).limit(5).all()
    unread_alerts = Alert.query.filter_by(user_id=current_user.id, acknowledged=False).all()
    
    return render_template('dashboard.html',
                         recent_vitals=recent_vitals,
                         recent_predictions=recent_predictions,
                         unread_alerts=unread_alerts,
                         now=datetime.now())

@main_bp.route('/live-data')
@login_required
def live_data():
    return render_template('live_data.html')

@main_bp.route('/prediction')
@login_required
def prediction():
    return render_template('prediction.html')

@main_bp.route('/chat')
@login_required
def chat():
    chat_history = ChatMessage.query.filter_by(user_id=current_user.id)\
        .order_by(ChatMessage.timestamp.desc()).limit(50).all()
    return render_template('chat.html', chat_history=chat_history)

@main_bp.route('/profile')
@login_required
def profile_view():
    return render_template('profile_view.html', user=current_user)

@main_bp.route('/profile/edit')
@login_required
def profile_edit():
    return render_template('profile_edit.html', user=current_user)

@main_bp.route('/download-report')
@login_required
def download_report():
    try:
        vitals = VitalRecord.query.filter_by(user_id=current_user.id)\
            .order_by(VitalRecord.timestamp.desc()).limit(30).all()
        predictions = Prediction.query.filter_by(user_id=current_user.id)\
            .order_by(Prediction.timestamp.desc()).limit(10).all()
        
        pdf_buffer = generate_health_report(current_user, vitals, predictions)
        
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=f"VitalHealth_Report_{current_user.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mimetype='application/pdf'
        )
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('main.dashboard'))


# ==================== API ROUTES ====================

@api_bp.route('/chat', methods=['POST'])
@login_required
def chat_api():
    data = request.get_json()
    user_message = data.get('message', '')
    
    msg = user_message.lower()
    if any(w in msg for w in ['stress', 'anxious']):
        response = "😌 Try 4-7-8 breathing: Inhale 4 sec, hold 7 sec, exhale 8 sec. Repeat 4 times."
    elif any(w in msg for w in ['sleep', 'insomnia']):
        response = "😴 Tips: Consistent schedule, no screens before bed, cool dark room."
    elif any(w in msg for w in ['heart', 'palpitations']):
        response = "❤️ Normal heart rate: 60-100 BPM. See doctor if concerned."
    elif any(w in msg for w in ['bp', 'blood pressure']):
        response = "🩸 Normal BP: <120/80. Exercise, low salt, limit alcohol."
    elif any(w in msg for w in ['exercise', 'workout']):
        response = "🏃 Aim for 150 min moderate exercise weekly. Start with daily walks."
    elif any(w in msg for w in ['diet', 'food']):
        response = "🥗 Eat vegetables, lean protein, whole grains. Drink 8 glasses water daily."
    else:
        response = "👋 I'm your AI Health Assistant! Ask about stress, sleep, heart, BP, exercise, or diet."
    
    chat = ChatMessage(user_id=current_user.id, user_message=user_message, bot_response=response)
    db.session.add(chat)
    db.session.commit()
    
    return jsonify({'response': response})

@api_bp.route('/predict', methods=['POST'])
@login_required
def predict():
    try:
        data = request.get_json()
        
        heart_rate = float(data.get('heart_rate'))
        spo2 = float(data.get('spo2'))
        temperature = float(data.get('temperature'))
        
        # Calculate risk score
        risk_score = 0
        recommendations = []
        
        if heart_rate > 100:
            risk_score += 20
            recommendations.append("❤️ Heart rate elevated - practice deep breathing")
        elif heart_rate < 60:
            risk_score += 10
            recommendations.append("❤️ Heart rate lower than normal - monitor")
        else:
            recommendations.append("❤️ Heart rate is normal")
        
        if spo2 < 90:
            risk_score += 40
            recommendations.append("💨 Critical low oxygen - seek medical help")
        elif spo2 < 95:
            risk_score += 25
            recommendations.append("💨 Low oxygen - deep breathing exercises")
        else:
            recommendations.append("💨 Oxygen level is normal")
        
        if temperature > 38.5:
            risk_score += 30
            recommendations.append("🌡️ High fever - rest and hydrate")
        elif temperature > 37.5:
            risk_score += 15
            recommendations.append("🌡️ Mild fever - rest and hydrate")
        elif temperature < 35.5:
            risk_score += 15
            recommendations.append("🌡️ Low temperature - keep warm")
        else:
            recommendations.append("🌡️ Temperature is normal")
        
        if risk_score >= 60:
            condition = "High Risk"
            risk_level = "High"
            confidence = 85
        elif risk_score >= 30:
            condition = "Moderate Risk"
            risk_level = "Moderate"
            confidence = 65
        else:
            condition = "Low Risk"
            risk_level = "Low"
            confidence = 85
        
        # Save vital record
        vital = VitalRecord(
            user_id=current_user.id,
            heart_rate=heart_rate,
            spo2=spo2,
            temperature=temperature
        )
        db.session.add(vital)
        db.session.commit()
        
        # Save prediction
        pred = Prediction(
            user_id=current_user.id,
            vital_record_id=vital.id,
            predicted_condition=condition,
            confidence_score=confidence,
            risk_level=risk_level,
            recommendations=json.dumps(recommendations)
        )
        db.session.add(pred)
        db.session.commit()
        
        # Create alert for high risk
        if risk_level == "High":
            alert = Alert(
                user_id=current_user.id,
                alert_type="critical",
                message=f"High risk detected! HR:{heart_rate}, SpO2:{spo2}, Temp:{temperature}"
            )
            db.session.add(alert)
            db.session.commit()
        
        return jsonify({
            'condition': condition,
            'confidence': confidence,
            'risk_level': risk_level,
            'recommendations': recommendations,
            'risk_score': risk_score
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@api_bp.route('/sensor-data', methods=['POST'])
def sensor_data():
    try:
        data = request.get_json()
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@api_bp.route('/historical-data')
@login_required
def historical_data():
    vitals = VitalRecord.query.filter_by(user_id=current_user.id)\
        .order_by(VitalRecord.timestamp.desc()).limit(50).all()
    return jsonify([{
        'timestamp': v.timestamp.isoformat(),
        'heart_rate': v.heart_rate,
        'spo2': v.spo2,
        'temperature': v.temperature
    } for v in vitals])

@api_bp.route('/alerts/acknowledge', methods=['POST'])
@login_required
def acknowledge_alerts():
    Alert.query.filter_by(user_id=current_user.id, acknowledged=False).update({'acknowledged': True})
    db.session.commit()
    return jsonify({'success': True})

@api_bp.route('/alerts/acknowledge/<int:alert_id>', methods=['POST'])
@login_required
def acknowledge_single_alert(alert_id):
    alert = Alert.query.get(alert_id)
    if alert and alert.user_id == current_user.id:
        alert.acknowledged = True
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False}), 404

@api_bp.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    current_user.age = request.form.get('age', type=int)
    current_user.gender = request.form.get('gender')
    current_user.height = request.form.get('height', type=float)
    current_user.weight = request.form.get('weight', type=float)
    current_user.smoker = request.form.get('smoker')
    current_user.alcohol_consumer = request.form.get('alcohol')
    current_user.exercise_frequency = request.form.get('exercise')
    
    db.session.commit()
    flash('Profile updated!', 'success')
    return redirect(url_for('main.profile_view'))

# @main_bp.route('/trends')
# @login_required
# def trends():
#     # Fetch all vitals and predictions
#     vitals = VitalRecord.query.filter_by(user_id=current_user.id)\
#         .order_by(VitalRecord.timestamp.desc()).all()
#     predictions = Prediction.query.filter_by(user_id=current_user.id)\
#         .order_by(Prediction.timestamp.desc()).all()
    
#     # Calculate averages
#     hr_values = [v.heart_rate for v in vitals if v.heart_rate]
#     spo2_values = [v.spo2 for v in vitals if v.spo2]
#     temp_values = [v.temperature for v in vitals if v.temperature]
    
#     avg_hr = round(sum(hr_values) / len(hr_values), 1) if hr_values else None
#     avg_spo2 = round(sum(spo2_values) / len(spo2_values), 1) if spo2_values else None
#     avg_temp = round(sum(temp_values) / len(temp_values), 1) if temp_values else None
    
#     # Generate insights
#     hr_insight = None
#     if avg_hr:
#         if avg_hr > 100:
#             hr_insight = f"Your average heart rate is {avg_hr} BPM, which is above the normal range. Consider stress reduction techniques and consult a doctor if persistent."
#         elif avg_hr < 60:
#             hr_insight = f"Your average heart rate is {avg_hr} BPM, which is below normal. Monitor for dizziness or fatigue."
#         else:
#             hr_insight = f"Your average heart rate is {avg_hr} BPM, which is within the healthy range. Keep up the good work!"
    
#     spo2_insight = None
#     if avg_spo2:
#         if avg_spo2 < 95:
#             spo2_insight = f"Your average SpO₂ is {avg_spo2}%, which is below optimal. Practice deep breathing exercises daily."
#         else:
#             spo2_insight = f"Your average SpO₂ is {avg_spo2}%, which is excellent! Maintain with regular deep breathing."
    
#     temp_insight = None
#     if avg_temp:
#         if avg_temp > 37.2:
#             temp_insight = f"Your average temperature is {avg_temp}°C, slightly elevated. Stay hydrated and monitor."
#         elif avg_temp < 36.1:
#             temp_insight = f"Your average temperature is {avg_temp}°C, slightly low. Keep warm and monitor."
#         else:
#             temp_insight = f"Your average temperature is {avg_temp}°C, which is normal."
    
#     bmi = current_user.get_bmi()
#     bmi_insight = None
#     if bmi:
#         if bmi < 18.5:
#             bmi_insight = f"Your BMI is {bmi}, indicating underweight. Consider nutritional counseling for healthy weight gain."
#         elif bmi < 25:
#             bmi_insight = f"Your BMI is {bmi}, which is in the healthy range. Maintain with balanced diet and exercise."
#         elif bmi < 30:
#             bmi_insight = f"Your BMI is {bmi}, indicating overweight. Focus on portion control and regular physical activity."
#         else:
#             bmi_insight = f"Your BMI is {bmi}, indicating obesity. Consult a healthcare provider for a weight management plan."
    
#     lifestyle_insight = None
#     if current_user.smoker == 'current':
#         lifestyle_insight = "Smoking is a major health risk. Consider smoking cessation programs for better health."
#     elif current_user.smoker == 'past':
#         lifestyle_insight = "Great job quitting smoking! Your health benefits continue to improve."
    
#     if current_user.alcohol_consumer == 'regular':
#         lifestyle_insight = (lifestyle_insight + " " if lifestyle_insight else "") + "Regular alcohol consumption increases health risks. Consider reducing to moderate levels."
    
#     if current_user.exercise_frequency == 'sedentary':
#         lifestyle_insight = (lifestyle_insight + " " if lifestyle_insight else "") + "Start with light physical activity like walking 10-15 minutes daily to improve health."
    
#     # Generate charts
#     hr_chart = create_heart_rate_chart(vitals[:50])
#     spo2_chart = create_spo2_chart(vitals[:50])
#     temp_chart = create_temperature_chart(vitals[:50])
#     risk_chart = create_risk_distribution_chart(predictions[:50])
#     vitals_comparison = create_vitals_comparison_chart(vitals[:50])
#     bmi_gauge = create_bmi_gauge(bmi)
#     activity_chart = create_activity_summary(current_user)
    
#     return render_template('trends.html',
#                          now=datetime.now(),
#                          hr_chart=hr_chart,
#                          spo2_chart=spo2_chart,
#                          temp_chart=temp_chart,
#                          risk_chart=risk_chart,
#                          vitals_comparison=vitals_comparison,
#                          bmi_gauge=bmi_gauge,
#                          activity_chart=activity_chart,
#                          total_records=len(vitals),
#                          avg_hr=avg_hr,
#                          avg_spo2=avg_spo2,
#                          avg_temp=avg_temp,
#                          hr_insight=hr_insight,
#                          spo2_insight=spo2_insight,
#                          temp_insight=temp_insight,
#                          bmi_insight=bmi_insight,
#                          lifestyle_insight=lifestyle_insight)
@main_bp.route('/trends')
@login_required
def trends():
    # Fetch all vitals
    vitals = VitalRecord.query.filter_by(user_id=current_user.id)\
        .order_by(VitalRecord.timestamp.desc()).all()
    
    # Fetch predictions for risk distribution
    predictions = Prediction.query.filter_by(user_id=current_user.id)\
        .order_by(Prediction.timestamp.desc()).all()
    
    # Generate charts
    hr_chart = create_heart_rate_chart(vitals)
    spo2_chart = create_spo2_chart(vitals)
    temp_chart = create_temperature_chart(vitals)
    risk_chart = create_risk_distribution_chart(predictions)
    
    # Generate summary stats
    stats = create_summary_stats(vitals)
    
    # Generate health insights
    insights = generate_insights(vitals, predictions, current_user)
    
    # Get latest readings
    latest = vitals[0] if vitals else None
    
    return render_template('trends.html',
                         now=datetime.now(),
                         hr_chart=hr_chart,
                         spo2_chart=spo2_chart,
                         temp_chart=temp_chart,
                         risk_chart=risk_chart,
                         stats=stats,
                         insights=insights,
                         latest=latest,
                         total_records=len(vitals))