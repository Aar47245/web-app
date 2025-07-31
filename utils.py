from models import db, User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def seed_admin():
    if not User.query.filter_by(role="Admin").first():
        hashed_pw = bcrypt.generate_password_hash("Admin@123").decode('utf-8')
        admin = User(username="admin", password=hashed_pw, role="Admin")
        db.session.add(admin)
        db.session.commit()
        print("Default admin created: admin / Admin@123")
