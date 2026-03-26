from app import create_app, db
from app.models import User, VitalRecord, Prediction, MedicalReport
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.create_all()
    print("Database tables created successfully!")

    test_user = User(
        username="testuser",
        email="test@example.com",
        password_hash=generate_password_hash("password123")
    )

    db.session.add(test_user)
    db.session.commit()

    print("Test user created successfully!")