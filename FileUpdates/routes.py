from flask import render_template, flash, redirect, url_for, session
from flask_login import current_user, login_user, logout_user
from app import app, db
from app.forms import LoginForm, RegistrationForm, UserPreferenceForm
from app.models import User
from app.user_profile_support.get_user_nutrients import *
from app.user_profile_support.get_userPreference_Answers import get_userPreferences
from app.user_profile_support.ingredientSubsitutions import run_master_ingredient_sub, get_recipe_list
import numpy as np

# TODO: Make user_profile_data global so list populated remain between loads and is doens;t have to recalculated everytime
# TODO: If user_profile_data cannot be global save recipei suggestion index to something that will persist

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
        return redirect(url_for('user_profile'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout',  methods=['GET', 'POST'])
def logout():
    logout_user()
    session.pop('data', None)
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user_profile'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# User Prefernce Survey
@app.route('/preference_survey')
def preference_survey():
   return render_template('survey.html', title='Preferences')


# Render User Profile page
@app.route('/user_profile')
# @login_required
def user_profile():
    if current_user.is_authenticated:
        user = current_user.username

        # TODO: get global user_profile_data if exist instead of overwriting old one
        if 'data' not in session.keys():
            session['data'] = get_userPreferences(user).to_json()
        
        user_profile_data = pd.read_json(session['data'])

        if user_profile_data is not False:

            # Calculate Micro and Macros for the User
            macros = get_macro_nutrients(user_profile_data)
            micros = get_micro_nutrients(user_profile_data)

            # Check if Recipe Suggetsions have been created for the user
            # If not, calclate and pass to profile to list
            print(user_profile_data.keys())
            print('list_keys' not in user_profile_data.keys())
            if 'list_keys' not in user_profile_data.keys():
                print("Getting Best Recipe Combo for the Week")
                best_recipe_combo, weekly_diet_amount, user_profile_data = get_recipe_list(user_profile_data, user)

                # TODO: Get names of recipes and not just index

            # Render the Users Profile Page
            return render_template('userProfile_existing.html', user_data=user_profile_data, macros=macros,micros=micros)
        else:
            # Render the New User SetUp page until they comlete prefernece
            return render_template('userProfile_new.html', title="User Preferneces", user=user)
        return redirect(url_for('index'))


# Links to page with recipe recommendations and ability to change out recipes
@app.route('/recipe_recommendation')
# @login_required
def recipe_recommendation():
    if current_user.is_authenticated:
        user = current_user.username
        # Check if user has completed user preferneces form
        # TODO: get global user_profile_data instead of overwriting old one
        #user_profile_data = get_userPreferences(user)

        user_profile_data = pd.read_json(session['data'])
        if user_profile_data is not False:
            # user_profile_data.meals_per_week = 6

            # Get Recipe Reccomendations for the user
            if 'list_keys' not in user_profile_data.keys():
                best_recipe_combo, weekly_diet_amount, user_profile_data = get_recipe_list(user_profile_data, user)

            print(user_profile_data.keys)
            # Sanity Check the ignore list before returning Results. If a recipe is in ignore list run again
            while any(np.intersect1d(user_profile_data.ignore_list, best_recipe_combo)):
                best_recipe_combo, weekly_diet_amount, user_profile_data = get_recipe_list(user_profile_data, user)

            # Render the Users Profile Page
            return render_template('recipe_recommendation.html', user_data=user_profile_data)
        else:
            # Render the New User SetUp page until they comlete prefernece
            return render_template('userProfile_existing.html', user_data=user_profile_data, macros=macros, micros=micros)
        return redirect(url_for('index'))


@app.route('/subsitute_ingredients')
def subsitute_ingredients():
    if current_user.is_authenticated:
        user = current_user.username
        # Check if user has recipies
        # TODO: get global user_profile_data if exist instead of overwriting old one
        #user_profile_data = get_userPreferences(user)

        user_profile_data = pd.read_json(session['data'])
        # filter_list
        if user_profile_data is not False:
            # Figure out interaction
            df, df_list = run_master_ingredient_sub(user_profile_data)

            # TODO: get single replacement for ingredient in UI
            # Render the Users Profile Page
            return render_template('subsitute_ingredients.html', user_data=user_profile_data,
            df=df, df_list=df_list)
        else:
            # Render the New User SetUp page until they comlete prefernece
            return render_template('userProfile_new.html', title="User Preferneces",
             user=user)
        return redirect(url_for('index'))


@app.route('/shopping_list')
def shopping_list():
    if current_user.is_authenticated:
        user = current_user.username
        # TODO: get global user_profile_data if exist instead of overwriting old one
        #user_profile_data = get_userPreferences(user)
        user_profile_data = pd.read_json(session['data'])
        if user_profile_data is not False:
            # Get Ingredient List to Create a Shopping List
            ingredient_list = []
            return render_template('shopping_list.html', ingredient_list=ingredient_list, user_data=user_profile_data)
        else:
            # Render the New User SetUp page until they comlete prefernece
            return render_template('userProfile_existing.html', title="User Profile",
             user=user)
        return redirect(url_for('index'))


# User Prefernece Form
# @app.route('/user_preferences', methods=['GET', 'POST'])
# def user_preferences():
#     if current_user.is_authenticated:
#         user = current_user.username
#         gender_list = ['Male', 'Female', 'Prefer Not to Say']
#         form = UserPreferenceForm()
#         if form.validate_on_submit():
#             user_pref = UserPreference(
#             username=user,
#             firstname=form.firstname.data,
#             lastname=form.lastname.data,
#             gender=form.gender.data,
#             age=form.age.data,
#             weight_lb=form.weight_lb.data,
#             height_in=form.height_in.data,
#             foods_allergic=form.foods_allergic.data
#             )
#             db.session.add(user_pref)
#             db.session.commit()
#             # flash('Congratulations, you are now a registered user!')
#             return redirect('/user_profile_existing')
#     return render_template('user_preferences.html', user=user, form=form, gender_list=gender_list)
