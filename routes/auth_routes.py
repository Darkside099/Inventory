# Authentication routes: register, login, logout using Flask-Login.
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models.models import User

auth_bp = Blueprint('auth', __name__, template_folder='../templates')

@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('inventory.dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form.get('role','Staff')
        if User.query.filter_by(username=username).first():
            flash('User already exists', 'warning')
            return redirect(url_for('auth.register'))
        user = User(username=username, password=generate_password_hash(password), role=role)
        db.session.add(user)
        db.session.commit()
        flash('Registered successfully. Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'info')
    return redirect(url_for('auth.login'))
