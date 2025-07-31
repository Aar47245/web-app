from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import db, User
from utils import seed_admin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['JWT_SECRET_KEY'] = 'jwtsecret'

db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Create tables + seed admin
with app.app_context():
    db.create_all()
    seed_admin()

# Register
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "User already exists"}), 400
    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(username=data['username'], password=hashed_pw, role="Student")
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Registered successfully"}), 201

# Login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        token = create_access_token(identity={"username": user.username, "role": user.role})
        return jsonify({"token": token, "role": user.role})
    return jsonify({"message": "Invalid credentials"}), 401

# Get all users (Admin only)
@app.route('/api/users', methods=['GET'])
@jwt_required()
def get_users():
    current_user = get_jwt_identity()
    if current_user['role'] != "Admin":
        return jsonify({"message": "Admin access only"}), 403
    users = [{"id": u.id, "username": u.username, "role": u.role} for u in User.query.all()]
    return jsonify(users)

# Create user (Admin only)
@app.route('/api/users', methods=['POST'])
@jwt_required()
def create_user():
    current_user = get_jwt_identity()
    if current_user['role'] != "Admin":
        return jsonify({"message": "Admin access only"}), 403
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "User already exists"}), 400
    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(username=data['username'], password=hashed_pw, role=data.get('role', 'Student'))
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created"}), 201

# Delete user (Admin only)
@app.route('/api/users/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    current_user = get_jwt_identity()
    if current_user['role'] != "Admin":
        return jsonify({"message": "Admin access only"}), 403
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
