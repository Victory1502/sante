import secrets
from datetime import datetime
from flask import Flask, flash, request, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import joblib  # Pour charger le modèle de prédiction
import os

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] ="postgresql://postgres:15022002@localhost:5433/esante"
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://workshop_owner:ajK6TuFNg5Qf@ep-withered-haze-a5aa2jwy-pooler.us-east-2.aws.neon.tech/workshop?sslmode=require"
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SESSION_TYPE'] = 'filesystem'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'patient' ou 'doctor'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, firstname, email, password, date_of_birth, role):
        self.name = name
        self.firstname = firstname
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        self.date_of_birth = date_of_birth
        self.role = role

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def add_user(self):
        db.session.add(self)
        db.session.commit()


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    symptoms = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')  # Statut du rendez-vous : 'pending', 'confirmed', 'completed'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, patient_id, doctor_id, appointment_date, symptoms):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.appointment_date = appointment_date
        self.symptoms = symptoms

    def add_appointment(self):
        db.session.add(self)
        db.session.commit()

    def update_status(self, new_status):
        self.status = new_status
        db.session.commit()