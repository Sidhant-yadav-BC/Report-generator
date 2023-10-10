from flask import Blueprint
from flask import render_template, request, flash, redirect, url_for
from .models import Users
from . import db
from werkzeug.security import  generate_password_hash, check_password_hash 
from flask_login import login_user, login_required, logout_user, current_user 


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username= request.form.get('username')
        password= request.form.get('password')
        
        user = Users.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True ) # keeps user logged in 
                # return redirect(url_for('user_view.home'))
                # return render_template('user_view.user_form.html', username=user.username)
                if user.role == "admin":
                    return redirect(url_for('admin_view.admin_landing'))
                else:
                    return redirect(url_for('user_view.user_form'))
            else:
                flash("Wrong username or password. Please try again",category='error')
                return redirect(url_for('auth.login'))
        else:
            flash("Wrong username or password. Please try again",category='error')
            return redirect(url_for('auth.login'))
             
    data= request.form
    return render_template('login.html')

@auth.route('/logout')
@login_required #makes sure logout can only be accessed if user is logged in
def logout():
    flash("Logged out succesfully",category='success')
    logout_user()#logs out user of session
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        
        # Check if a user with the same username or email already exists
        existing_user = Users.query.filter_by(username=username).first()
        existing_email = Users.query.filter_by(email=email).first()
        
        # Validate input fields
        if existing_user:
            flash('Username already exists. Please try a different username.', category='error')
            return redirect(url_for('auth.signup'))
        elif existing_email:
            flash('Email is already in use. Please use a different email address.', category='error')
            return redirect(url_for('auth.signup'))
        elif len(email) < 4:
            flash('Email must be at least 4 characters long.', category='error')
        elif len(username) < 4:
            flash('Username must be at least 4 characters long.', category='error')
        else:
            # Create a new user
            new_user = Users(email=email, username=username, password=generate_password_hash(password, method="sha256"), role = role)
            
            # Add the user to the database
            db.session.add(new_user)
            db.session.commit()
            
            # Log in the new user after registration
            login_user(new_user, remember=True)
            
            flash("Account created successfully. You are now logged in.", category='success')
            if(new_user.role=='user'):
                return redirect(url_for('user_view.user_form'))
            else:
                return redirect(url_for('admin_view.admin_landing'))
    
    return render_template('sign_up.html')

    