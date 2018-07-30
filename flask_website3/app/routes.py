from app import app, db
from flask import render_template, flash, redirect, url_for, session, request
from flask_login import current_user, login_user, logout_user
from app.forms import LoginForm, RegistrationForm, UserPreferenceForm
from app.models import User, InputMacroNutrientsForm, InputMicroNutrientsForm, IgnoreRecipeForm, IngredientSubForm
from app.user_profile_support.get_user_nutrients import *
from app.user_profile_support.get_userPreference_Answers import *
from app.user_profile_support.ingredientSubsitutions import *
import numpy as np
# import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
# import matplotlib.pyplot as plt

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
    print(session.keys())
    session.pop('data', None)
    session.pop('ignore_list', None)
    session.pop('user_id', None)
    session.pop('user_meal_plan', None)
    session.pop('micros', None)
    session.pop('macros', None)
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
        login_user(user)
        return redirect(url_for('user_profile'))
    return render_template('register.html', title='Register', form=form)


# User Prefernce Survey
@app.route('/preference_survey')
def preference_survey():
   return render_template('survey.html', title='Preferences')


# Render User Profile page
@app.route('/user_profile', methods=['GET', 'POST'])
# @login_required
def user_profile():
    if current_user.is_authenticated:
        user = current_user.username

        if 'data' not in session.keys():
            # Get user prefernces from form if the session dat ahas not yet been populated
            data = get_userPreferences(user)
            if data is not False:
                session['data'] = data.to_json()

        if 'data' in session.keys():
            user_profile_data = pd.read_json(session['data'])

            # Calculate or Load Micro and Macros for the User
            if 'macros' not in session.keys():
                macros = get_macro_nutrients(session)
            if 'micros' not in session.keys():
                micros = get_micro_nutrients(session)
            macros = pd.read_json(session['macros'])
            micros = pd.read_json(session['micros'])

            # Check if Recipe Suggestions have been created for the user
            # If not, calclate and pass to profile to list
            if 'user_meal_plan' not in session.keys():
                best_recipe_combo, weekly_diet_amount, user_profile_data, df_ingredient_NDB = get_recipe_list(session, user)

            user_meal_plan = pd.read_json(session['user_meal_plan'])
            print(user_meal_plan)
            # Check to make sure recipes are not in the ignore list
            ignore_list = get_user_ignore_responses(user_profile_data, user)
            while any(np.intersect1d(ignore_list, user_meal_plan.recipe_id)):
                best_recipe_combo, weekly_diet_amount, user_profile_data, df_ingredient_NDB = get_recipe_list(session, user)
                user_meal_plan = pd.read_json(session['user_meal_plan'])

            print("HERE")
            print(user_meal_plan)
            macros_form = InputMacroNutrientsForm(request.form)
            micros_form = InputMicroNutrientsForm(request.form)
            if request.method == 'POST':
                macros, micros = process_nutrient_edit_form(macros_form.data, micros_form.data, macros, micros)
                # Save micro and Macro edited list for later fram
                session['macros'] = pd.DataFrame(macros).to_json()
                session['micros'] = pd.DataFrame(micros, index=[0]).to_json()
                # Render the Users Profile Page
                print(user_meal_plan)
                return render_template('userProfile_existing.html', user_data=user_profile_data, macros=macros, micros=micros, user_meal_plan=user_meal_plan, form1=macros_form, form2=micros_form)
            else:
                return render_template('userProfile_existing.html', user_data=user_profile_data, macros=macros, micros=micros, user_meal_plan=user_meal_plan, form1=macros_form, form2=micros_form)
        else:
            # Render the New User Landing page until they complete Preferneces Survey
            return render_template('userProfile_new.html', title="User Preferneces", user=user)
        return redirect(url_for('index'))


# Links to page with recipe recommendations and ability to change out recipes
@app.route('/recipe_recommendation', methods=['GET', 'POST'])
# @login_required
def recipe_recommendation():
    if current_user.is_authenticated:
        user = current_user.username

        user_profile_data = pd.read_json(session['data'])
        if user_profile_data is not False:
            # Get Recipe Reccomendations for the user
            if 'user_meal_plan' not in session.keys():
                best_recipe_combo, weekly_diet_amount, user_profile_data, df_ingredient_NDB = get_recipe_list(session, user)

            user_meal_plan = pd.read_json(session['user_meal_plan'])
            best_recipe_combo = user_meal_plan.recipe_id

            # Sanity Check the ignore list before returning Results. If a recipe is in ignore list run again
            ignore_list = get_user_ignore_responses(user_profile_data, user)
            if 'ignore_list' in session.keys():
                old_ignore_list = create_ignore_list_from_session_df(session)
                ignore_list = ignore_list + old_ignore_list
            session['ignore_list'] = pd.DataFrame({'recipe_ignore':ignore_list}).to_json()

            while any(np.intersect1d(ignore_list, user_meal_plan.recipe_id)):
                best_recipe_combo, weekly_diet_amount, user_profile_data, df_ingredient_NDB = get_recipe_list(session, user)
                user_meal_plan = pd.read_json(session['user_meal_plan'])

            #### Here is where plot needs to be called and saved off for jpg
            # fig = plt.figure()
            # ax = plt.axes()
            # x = np.linspace(0, 10, 1000)
            # ax.plot(x, np.sin(x))
            # fig.savefig('app/static/images/plot.png')

            ignore_form = IgnoreRecipeForm(request.form)
            if request.method == 'POST':
                process_ignore_form(session, ignore_form)
                # Render the Users Profile Page
                return render_template('recipe_recommendation.html', user_data=user_profile_data, user_meal_plan=user_meal_plan, ignore_form=ignore_form)
            else:
                print(request.method)
                return render_template('recipe_recommendation.html', user_data=user_profile_data, user_meal_plan=user_meal_plan, ignore_form=ignore_form)
        else:
            # Render the New User SetUp page until they comlete prefernece
            return render_template('userProfile_existing.html', user_data=user_profile_data, macros=macros, micros=micros)
        return redirect(url_for('index'))


# TODO: Make a form for user input
@app.route('/single_ingredient_replacement', methods=['GET', 'POST'])
def single_ingredient_replacement():
    # TODO: imporve UI into click to choose ingredient
    if current_user.is_authenticated:
        user = current_user.username
        # Check if user has recipies (DO I NEED TO DO THIS?)
        # user_profile_data = pd.read_json(session['data'])
        if pd.read_json(session['data']) is not False:
            # Figure out interaction
            user_meal_plan = pd.read_json(session['user_meal_plan'])
            best_recipe_combo = user_meal_plan.recipe_id

            ingredientSubForm = IngredientSubForm(request.form)
            recipe_id=best_recipe_combo[0]
            df_ingredient_NDB = get_ingredient_NDB_number(session, best_recipe_combo)
            df_ingredient_NDB = df_ingredient_NDB[df_ingredient_NDB.recipe_id == recipe_id]

            if request.method == 'POST':
                print("POST")
                print(ingredientSubForm.ingredientSub.data)
                df, df_list = get_single_ingredient_replacement(session, ingredientSubForm.ingredientSub.data,  recipe_id)
                # Render the Users Profile Page
                return render_template('subsitute_ingredients.html', form=ingredientSubForm, ingredient_list=ingredient_list)

                # return render_template('subsitute_ingredients.html', user_data=pd.read_json(session['data']), df=df, df_list=df_list)
            else:
                # Displays Ingredients User Can Choose to Replace
                return render_template('subsitute_ingredients.html', form=ingredientSubForm, df_ingredient_NDB=df_ingredient_NDB)
                # return render_template('subsitute_ingredients.html', user_data=pd.read_json(session['data']), df=df, df_list=df_list)

            # print(session.keys())
            # print("HEREEE")
            #
            #
            # # TODO: get single replacement for ingredient in UI
            # # Render the Users Profile Page
            # print("HERE")
            # return render_template('subsitute_ingredients.html', user_data=pd.read_json(session['data']), df=df, df_list=df_list)
        else:
            # Render the New User SetUp page until they comlete prefernece
            return render_template('userProfile_new.html', title="User Preferneces",
             user=user)
        return redirect(url_for('index'))


# Force Rerun of Recipe Plan and Display on User Profile Page
@app.route('/rerun_recipe_plan')
def rerun_recipe_plan():
    user = current_user.username
    best_recipe_combo, weekly_diet_amount, user_profile_data, df_ingredient_NDB  = get_recipe_list(session, user)
    # session['df_ingredient_NDB'] = df_ingredient_NDB.to_json()
    return redirect(url_for('user_profile'))


# Reset Goals to Default
@app.route('/reset_nutrient_goals')
def reset_nutrient_goals():
    # Recalculate nutrient goals and rerout to page
    macros = get_macro_nutrients(session)
    micros = get_micro_nutrients(session)

    macros_form = InputMacroNutrientsForm(request.form)
    micros_form = InputMicroNutrientsForm(request.form)
    return redirect(url_for('user_profile'))
    # return render_template("edit_nutrients.html", form1=macros_form, form2=micros_form, macros=macros, micros=micros)


@app.route('/display_recipe')
def display_recipe():
    if current_user.is_authenticated:
        user = current_user.username

        user_profile_data = pd.read_json(session['data'])
        if user_profile_data is not False:
            # Get Recipes, ingredients and instructions
            # try:
            user_meal_plan = pd.read_json(session['user_meal_plan'])
            best_recipe_combo = user_meal_plan.recipe_id
            recipe_details = get_recipe_details(best_recipe_combo, user_profile_data)
            # except:
            #     recipe_details = []
            print("recipe Details")
            print(len(recipe_details), type(recipe_details))
            print(recipe_details[0].get('name'))
            for pos in recipe_details:
                print(pos)
            return render_template('display_recipe.html', user_data=user_profile_data, recipe_details=recipe_details)
        else:
            # Render the New User SetUp page until they comlete prefernece
            return render_template('userProfile_existing.html', title="User Profile",
             user=user)
        return redirect(url_for('index'))



@app.route('/shopping_list')
def shopping_list():
    if current_user.is_authenticated:
        user = current_user.username

        user_profile_data = pd.read_json(session['data'])
        if user_profile_data is not False:
            # Get Ingredient List to Create a Shopping List
            try:
                user_meal_plan = pd.read_json(session['user_meal_plan'])
                best_recipe_combo = user_meal_plan.recipe_id
                ingredient_list = get_shopping_list(best_recipe_combo, user_profile_data)
            except:
                ingredient_list = []
            return render_template('shopping_list.html', ingredient_list=ingredient_list, user_data=user_profile_data)
        else:
            # Render the New User SetUp page until they comlete prefernece
            return render_template('userProfile_existing.html', title="User Profile",
             user=user)
        return redirect(url_for('index'))



# @app.route('/edit_nutrients', methods=['GET', 'POST'])
# def edit_nutrients():
#     if current_user.is_authenticated:
#         user = current_user.username
#         user_profile_data = pd.read_json(session['data'])
#         macros = pd.read_json(session['macros'])
#         micros = pd.read_json(session['micros'])
#
#     macros_form = InputMacroNutrientsForm(request.form)
#     micros_form = InputMicroNutrientsForm(request.form)
#     if request.method == 'POST':
#         macros, micros = process_nutrient_edit_form(macros_form.data, micros_form.data, macros, micros)
#
#         # Save micro and Macro edited list for later fram
#         session['macros'] = pd.DataFrame(macros).to_json()
#         session['micros'] = pd.DataFrame(micros, index=[0]).to_json()
#
#         return render_template("edit_nutrients.html", form1=macros_form, form2=micros_form, macros=macros, micros=micros)
#     else:
#         return render_template("edit_nutrients.html", form1=macros_form, form2=micros_form, macros=macros, micros=micros)

@app.route('/food_network', methods=['GET', 'POST'])
def food_network():
    return render_template('data.html', title="Graph Test")
