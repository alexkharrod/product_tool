from application import create_app, db
import application.models  # Ensure all models are registered

app = create_app()
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")
