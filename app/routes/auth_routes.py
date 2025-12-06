from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user
from ..extensions import db, bcrypt
from ..model.user_model import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists.', 'danger')
            return redirect(url_for('auth.register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.home'))
        else:
            flash('Login unsuccessful. Check username and password.', 'danger')

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))