from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user
from app import app
from app.forms import LoginForm, RegistrationForm
from app.models import User
from app import db

@app.route('/')
@app.route('/index')

def index():
    return render_template('indexWorking.html')

@app.route('/about')

def about():
    return render_template('about_the_project.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('user_profile_new'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout',  methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user_profile_new'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# Render User Profile page
@app.route('/user_profile_new')
def user_profile_new():
    if current_user.is_authenticated:
        # How do I query the User Model?
        # user = User.query.filter_by(username=username.data).first()
        user = 'Johnny Appleseed' # Fix this to be Dynamic
        return render_template('userProfile_new.html', user=user)
    return redirect(url_for('index'))


# Render the User Preferneces Form To Set Up Account
# @app.route('/')
# def user_profile_new():
#     if current_user.is_authenticated:
#         # How do I query the User Model?
#         user = 'User' # Fix this to be Dynamic
#         return render_template('userProfile_new.html', user=user)
#     return redirect(url_for('index'))




# Render User Profile After User Has Set Up preferneces
# Note! This is a fake - needs to be changed to dynamic
@app.route('/user_profile_existing')
def user_profile_existing():
    if current_user.is_authenticated:
        # How do I query the User Model?
        user = 'Johnny' # Fix this to be Dynamic
        return render_template('userProfile_existing.html', user=user)
    return redirect(url_for('index'))
