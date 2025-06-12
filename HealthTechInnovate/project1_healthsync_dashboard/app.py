from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from dateutil.parser import parse
from models import db, User, Appointment, Medication, Vital
from utils import login_required
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/healthsync.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
        else:
            hashed_password = generate_password_hash(password)
            user = User(username=username, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid username or password.', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    appointments = Appointment.query.filter_by(user_id=user_id).order_by(Appointment.date.asc()).limit(5).all()
    medications = Medication.query.filter_by(user_id=user_id).order_by(Medication.time.asc()).limit(5).all()
    vitals = Vital.query.filter_by(user_id=user_id).order_by(Vital.date.desc()).limit(5).all()
    return render_template('dashboard.html', appointments=appointments, medications=medications, vitals=vitals)

@app.route('/appointments', methods=['GET', 'POST'])
@login_required
def appointments():
    if request.method == 'POST':
        date = parse(request.form['date'])
        description = request.form['description']
        user_id = session['user_id']
        appointment = Appointment(user_id=user_id, date=date, description=description)
        db.session.add(appointment)
        db.session.commit()
        flash('Appointment added.', 'success')
        return redirect(url_for('appointments'))
    appointments = Appointment.query.filter_by(user_id=session['user_id']).all()
    return render_template('appointments.html', appointments=appointments)

@app.route('/appointments/delete/<int:id>', methods=['POST'])
@login_required
def delete_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    if appointment.user_id != session['user_id']:
        flash('Unauthorized action.', 'error')
        return redirect(url_for('appointments'))
    db.session.delete(appointment)
    db.session.commit()
    flash('Appointment deleted.', 'success')
    return redirect(url_for('appointments'))

@app.route('/medications', methods=['GET', 'POST'])
@login_required
def medications():
    if request.method == 'POST':
        name = request.form['name']
        dosage = request.form['dosage']
        time = parse(request.form['time'])
        user_id = session['user_id']
        medication = Medication(user_id=user_id, name=name, dosage=dosage, time=time)
        db.session.add(medication)
        db.session.commit()
        flash('Medication added.', 'success')
        return redirect(url_for('medications'))
    medications = Medication.query.filter_by(user_id=session['user_id']).all()
    return render_template('medications.html', medications=medications)

@app.route('/vitals', methods=['GET', 'POST'])
@login_required
def vitals():
    if request.method == 'POST':
        blood_pressure = request.form['blood_pressure']
        weight = float(request.form['weight'])
        date = datetime.now()
        user_id = session['user_id']
        vital = Vital(user_id=user_id, blood_pressure=blood_pressure, weight=weight, date=date)
        db.session.add(vital)
        db.session.commit()
        flash('Vitals recorded.', 'success')
        return redirect(url_for('vitals'))
    vitals = Vital.query.filter_by(user_id=session['user_id']).all()
    return render_template('vitals.html', vitals=vitals)

# REST API Endpoints
@app.route('/api/appointments', methods=['GET'])
@login_required
def api_appointments():
    appointments = Appointment.query.filter_by(user_id=session['user_id']).all()
    return jsonify([{'id': a.id, 'date': a.date.isoformat(), 'description': a.description} for a in appointments])

@app.route('/api/medications', methods=['GET'])
@login_required
def api_medications():
    medications = Medication.query.filter_by(user_id=session['user_id']).all()
    return jsonify([{'id': m.id, 'name': m.name, 'dosage': m.dosage, 'time': m.time.isoformat()} for m in medications])

@app.route('/api/vitals', methods=['GET'])
@login_required
def api_vitals():
    vitals = Vital.query.filter_by(user_id=session['user_id']).all()
    return jsonify([{'id': v.id, 'blood_pressure': v.blood_pressure, 'weight': v.weight, 'date': v.date.isoformat()} for v in vitals])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)