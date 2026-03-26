# init_db.py
from app import create_app, db
from app.models import User, VitalRecord, Prediction, MedicalReport, Alert, ChatMessage

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Database tables created successfully!")
    print("Tables created:")
    print("  - User")
    print("  - VitalRecord")
    print("  - Prediction")
    print("  - MedicalReport")
    print("  - Alert")
    print("  - ChatMessage")