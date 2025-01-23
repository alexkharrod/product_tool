from application import create_app, db
from application.models.user import User, Role
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Create admin user with proper security
    if not User.query.filter_by(email='aharrod@logoincluded.com').first():
        admin = User(
            email='aharrod@logoincluded.com',
            password_hash=generate_password_hash('TempPass123!'),
            role=Role.ADMIN
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully")
    else:
        print("Admin user already exists")
