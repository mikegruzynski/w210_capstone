from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user
from app import app
from app.forms import LoginForm, RegistrationForm, UserPreferenceForm
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
# @login_required
def user_profile_new():
    if current_user.is_authenticated:
        user = current_user.username # TODO: Change to real name when we get it
        return render_template('userProfile_new.html', title="User Preferneces", user=user)
    return redirect(url_for('index'))


# User Prefernece Form
@app.route('/user_preferences', methods=['GET', 'POST'])
def user_preferences():
    if current_user.is_authenticated:
        user = current_user.username
        form = UserPreferenceForm()
        gender_list = ['Male', 'Female', 'Prefer Not to Say']
        return render_template('user_preferences.html', user=user, form=form, gender_list=gender_list)
    #     if form.validate_on_submit():
    #         user_pref = UserPreference(
    #         username=form.username.data,
    #         firstname=form.firstname.data,
    #         lastname=form.lastname.data,
    #         gender=form.gender.data,
    #         age=form.age.data,
    #         weight_lb=form.weight_lb.data,
    #         height_in=form.height_in.data,
    #         foods_allergic=form.foods_allergic.data
    #         )
    #         db.session.add(user_pref)
    #         db.session.commit()
    #         flash('Congratulations, you are now a registered user!')
    #         return redirect(url_for('user_profile_existing'))
    # return redirect(url_for('user_preferences'))



# Render User Profile After User Has Set Up preferneces
# Note! This is a fake - needs to be changed to dynamic
@app.route('/user_profile_existing')
# @login_required
def user_profile_existing():
    if current_user.is_authenticated:
        user = current_user.username
        return render_template('userProfile_existing.html', user=user)
    return redirect(url_for('index'))
