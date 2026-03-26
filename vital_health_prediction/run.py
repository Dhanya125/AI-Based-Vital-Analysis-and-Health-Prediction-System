# run.py
from app import create_app, db
from app.models import User, VitalRecord, Prediction, MedicalReport, Alert, ChatMessage

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)