from flask import Flask, render_template, request, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = "frontendsecret"
BACKEND_URL = "http://127.0.0.1:5000/api"

@app.route('/')
def home():
    if 'token' in session:
        return render_template("welcome.html", username=session['username'], role=session['role'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        res = requests.post(f"{BACKEND_URL}/login", json={
            "username": request.form['username'],
            "password": request.form['password']
        })
        if res.status_code == 200:
            data = res.json()
            session['token'] = data['token']
            session['username'] = request.form['username']
            session['role'] = data['role']
            return redirect(url_for('home'))
        return "Login failed"
    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        res = requests.post(f"{BACKEND_URL}/register", json={
            "username": request.form['username'],
            "password": request.form['password']
        })
        if res.status_code == 201:
            return redirect(url_for('login'))
        return res.json().get("message", "Error")
    return render_template("register.html")

@app.route('/admin')
def admin_dashboard():
    if 'role' in session and session['role'] == "Admin":
        res = requests.get(f"{BACKEND_URL}/users", headers={"Authorization": f"Bearer {session['token']}"})
        if res.status_code == 200:
            return render_template("admin.html", users=res.json())
        return "Error loading users"
    return "Unauthorized", 403

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(port=5001, debug=True)

