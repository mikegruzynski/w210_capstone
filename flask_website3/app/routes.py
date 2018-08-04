from app import app, db
from flask import render_template, flash, redirect, url_for, session, request
from flask_login import current_user, login_user, logout_user
from app.forms import LoginForm, RegistrationForm, UserPreferenceForm
# from app.models import User, InputMacroNutrientsForm, InputMicroNutrientsForm, IgnoreRecipeForm, IngredientSubForm, ChooseRecipeToSubIngredients
from app.models import *
from app.user_profile_support.get_user_nutrients import *
from app.user_profile_support.get_userPreference_Answers import *
from app.user_profile_support.ingredientSubsitutions import *
from app.user_profile_support.get_recipe_center_data import *

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
    msg = ""
    print("Login")
    print("is authenticated", current_user.is_authenticated)
    if current_user.is_authenticated:
        return redirect(url_for('user_profile'))
    form = LoginForm()
    print("Login page")
    if form.validate_on_submit():
        print(form.username.data)
        user = User.query.filter_by(username=form.username.data).first()
        print("user", user)
        # print(user.check_password(form.password.data))
        try:
            if user is None or not user.check_password(form.password.data):
                print("Not Valid")
                msg = "We did not recognize your username. Please try again or go to regsitration page to register."
                flash('Invalid username or password')
                return render_template('login.html', title='Sign In', form=form, msg=msg)
            login_user(user, remember=form.remember_me.data)
        except:
            msg = "We did not recognize your username. Please try again or go to regsitration page to register."
            return render_template('login.html', title='Sign In', form=form, msg=msg)

        return redirect(url_for('user_profile'))
    return render_template('login.html', title='Sign In', form=form, msg=msg)


@app.route('/logout',  methods=['GET', 'POST'])
def logout():
    logout_user()
    print(session.keys())
    if 'data' in session.keys():
        session.pop('data', None)
    if 'ignore_list' in session.keys():
        session.pop('ignore_list', None)
    if 'user_id' in session.keys():
        session.pop('user_id', None)
    if 'user_meal_plan' in session.keys():
        session.pop('user_meal_plan', None)
    if 'micros' in session.keys():
        session.pop('micros', None)
    if 'macros' in session.keys():
        session.pop('macros', None)
    if 'df_ingredient_NDB' in session.keys():
        session.pop('df_ingredient_NDB', None)
    if 'pantry_items_list' in session.keys():
        session.pop('pantry_items_list', None)
    if 'pantry_recipe_ids' in session.keys():
        session.pop('pantry_recipe_ids', None)
    if 'switch_df_temp' in session.keys():
        session.pop('switch_df_temp', None)
    return redirect(url_for('index'))

# User Registraions
# TODO: clear form data after registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('user_profile'))
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            print("Try Register")
            user = User(username=form.username.data, email=form.email.data)
            print(user)
            user.authenticated=True
            print("User is authenticated")
            user.set_password(form.password.data)
            db.session.add(user)
            print("User is added to session")
            db.session.commit()
            print("User is comitted to session")
            flash('Congratulations, you are now a registered user!')

            login_user(user)
            print("User Logged in")
            return redirect(url_for('user_profile'))
        except:
            print("ERROR")
            db.session.rollback()
            msg = "We apologize, There has been an error with Regsitraion. Please Try again"

    return render_template('register.html', title='Register', form=form)


# User Prefernce Survey
@app.route('/preference_survey')
def preference_survey():
    print(current_user.is_authenticated)
    if current_user.is_authenticated:
        user = current_user.username
        print(user)
        return render_template('survey.html', title='Preferences', user=user)
    else:
        return redirect(url_for('register'))


# Render User Profile page
@app.route('/user_profile', methods=['GET', 'POST'])
def user_profile():
    print(current_user.is_authenticated)
    if current_user.is_authenticated:
        user = current_user.username
        if 'data' not in session.keys():
            print("Data is not in session keys")
            # Get user prefernces from form if the session dat ahas not yet been populated
            try:
                data = get_userPreferences(user)
            except:
                data = False
            if data is not False:
                session['data'] = data.to_json()
            print('data' in session.keys())

        if 'data' in session.keys():
            print("Data is in session keys")
            user_profile_data = pd.read_json(session['data'])

            # Calculate or Load Micro and Macros for the User
            if 'macros' not in session.keys():
                macros = get_macro_nutrients(session)
            if 'micros' not in session.keys():
                micros = get_micro_nutrients(session)
            macros = pd.read_json(session['macros'])
            micros = pd.read_json(session['micros'])
            print("Micros and Macros Calculated")
            # Check if Recipe Suggestions have been created for the user
            # If not, calclate and pass to profile to list

            if 'user_meal_plan' not in session.keys():
                print("user_meal_plan not in keys")
                best_recipe_combo, weekly_diet_amount, user_profile_data, df_ingredient_NDB = get_recipe_list(session, user)
            user_meal_plan = pd.read_json(session['user_meal_plan'])
            print("user_meal_plan calculated")
            # Check to make sure recipes are not in the ignore list
            ignore_list = get_user_ignore_responses(user_profile_data, user)
            while any(np.intersect1d(ignore_list, user_meal_plan.recipe_id)):
                best_recipe_combo, weekly_diet_amount, user_profile_data, df_ingredient_NDB = get_recipe_list(session, user)
                user_meal_plan = pd.read_json(session['user_meal_plan'])

            # macros_form = InputMacroNutrientsForm(request.form)
            # micros_form = InputMicroNutrientsForm(request.form)

            if request.method == 'POST':
                print("POST ")
                macros, micros = process_nutrient_edit_form(macros_form.data, micros_form.data, macros, micros)
                # Save micro and Macro edited list for later fram
                session['macros'] = pd.DataFrame(macros).to_json()
                session['micros'] = pd.DataFrame(micros, index=[0]).to_json()

                # Render the Users Profile Page
                return render_template('userProfile_existing.html', user_data=user_profile_data, macros=macros, micros=micros, user_meal_plan=user_meal_plan.values)
            else:
                print(request.method)
                return render_template('userProfile_existing.html', user_data=user_profile_data, macros=macros, micros=micros, user_meal_plan=user_meal_plan.values)
        else:
            print("data does not exist ")
            print(session.keys())
            # Render the New User Landing page until they complete Preferneces Survey
            return render_template('userProfile_new.html', title="User Preferneces", user=user)
    return redirect(url_for('index'))


## Recipe Center ----------------------------------------------
# Routes and infromation refering to recipes and meal plans
@app.route('/recipe_center', methods=['GET', 'POST'])
def recipe_center():
    if current_user.is_authenticated:
        user = current_user.username

        # Get Recipes Details with Name, Ingredients, Instructions
        user_profile_data = pd.read_json(session['data'])
        user_meal_plan = pd.read_json(session['user_meal_plan'])
        best_recipe_combo = user_meal_plan.recipe_id
        recipe_details = get_recipe_details(best_recipe_combo, user_profile_data)
        user_profile_data = pd.read_json(session['data'])

        if user_profile_data is not False:
            user_meal_plan = return_user_meal_plan(session, user_profile_data, user)
        print("user_meal_plan", user_meal_plan)

        return render_template('recipe_center_page.html', user_data=user_profile_data, recipe_details=recipe_details, user_meal_plan=user_meal_plan)
    else:
        # Render the New User SetUp page until they comlete prefernece
        return redirect(url_for('recipe_center'))
        # return render_template('userProfile_existing.html', user_data=user_profile_data, macros=macros, micros=micros, user_meal_plan=user_meal_plan.values, form1=macros_form, form2=micros_form)
    return redirect(url_for('index'))


@app.route('/display_recipe',  methods=['GET', 'POST'])
def display_recipe():
    if current_user.is_authenticated:
        user = current_user.username
        user_profile_data = pd.read_json(session['data'])
        pantry_recipe_ids = session['pantry_recipe_ids']
        best_recipe_combo = []
        for id in pantry_recipe_ids:
            best_recipe_combo.append("RECIPE_"+str(id))

        recipe_details = get_recipe_details(best_recipe_combo, user_profile_data)
        return render_template('display_recipe.html', user_data=user_profile_data, recipe_details=recipe_details)
    else:
        # Render the New User SetUp page until they comlete prefernece
        return render_template('userProfile_existing.html', title="User Profile",
         user=user)
    return redirect(url_for('index'))


# Links to page with recipe recommendations and ability to change out recipes
@app.route('/recipe_recommendation', methods=['GET', 'POST'])
# @login_required
def recipe_recommendation():
    if current_user.is_authenticated:
        user = current_user.username

        user_profile_data = pd.read_json(session['data'])
        if user_profile_data is not False:
            user_meal_plan = return_user_meal_plan(session, user_profile_data, user=user)
            update_text = ''

            #### Here is where plot needs to be called and saved off for jpg
            # fig = plt.figure()
            # ax = plt.axes()
            # x = np.linspace(0, 10, 1000)
            # ax.plot(x, np.sin(x))
            # fig.savefig('app/static/images/plot.png')

            # Form and route to ignore Recipes from list
            ignore_form = IgnoreRecipeForm(request.form)
            # Form for Ingredient Swap Page
            recipeNameIdForm = ChooseRecipeToSubIngredients(request.form)
            if request.method == 'POST':
                # Ingredient Replacment Request
                if recipeNameIdForm.recipe_name.data is not '':
                    best_recipe_combo = user_meal_plan.recipe_id
                    recipe_details = get_recipe_details(best_recipe_combo, user_profile_data)

                    recipe_id = recipeNameIdForm.recipe_name.data
                    for itr, details in enumerate(recipe_details):
                        if recipe_details[itr].get('name') == recipeNameIdForm.recipe_name.data:
                            recipe_id = recipe_details[itr].get('id')
                            break

                    # single_ingredient_replacement(recipe_id)
                    return redirect(url_for('single_ingredient_replacement', recipe_id=recipe_id))
                else:
                    # Ignore ingredient request
                    print("**TODO: Clear box when submitted")
                    # TODO: clear input box after submit
                    process_ignore_form(session, ignore_form)
                    # Render the Users Profile Page
                    update_text = 'Sorry you did not like the recipes! You will not see it again. Regenerate your recipe plan for new suggestions'
                    # return redirect(url_for('recipe_recommendation'))
                    return render_template('recipe_recommendation.html', user_data=user_profile_data, user_meal_plan=user_meal_plan, ignore_form=ignore_form, form2=recipeNameIdForm, update_text=update_text)
            else:
                return render_template('recipe_recommendation.html', user_data=user_profile_data, user_meal_plan=user_meal_plan, ignore_form=ignore_form, form2=recipeNameIdForm, update_text=update_text)
        else:
            # Render the New User SetUp page until they comlete prefernece
            return render_template('userProfile_existing.html', user_data=user_profile_data, macros=macros, micros=micros)
        return redirect(url_for('index'))

# TODO: visualizations
@app.route('/single_ingredient_replacement/<recipe_id>', methods=['GET', 'POST'])
def single_ingredient_replacement(recipe_id):
    if current_user.is_authenticated:
        user = current_user.username
        if pd.read_json(session['data']) is not False:

            # Get user meal plan from session
            user_meal_plan = pd.read_json(session['user_meal_plan'])
            best_recipe_combo = user_meal_plan.recipe_id

            # Get input Form from models for html
            choices = ['one','two', 'three']
            ingredientSubForm = IngredientSubForm(request.form)
            recipe_id_exp = "RECIPE_"+str(recipe_id) # Recipe User is choosing to Edit

            # Get Ingredients from Recipe as options to replace
            if 'df_ingredient_NDB' not in session.keys():
                df_ingredient_NDB = get_ingredient_NDB_number(session, best_recipe_combo)
                session['df_ingredient_NDB'] = df_ingredient_NDB.to_json()
            else:
                df_ingredient_NDB = pd.read_json(session['df_ingredient_NDB'])
            df_ingredient_NDBi = df_ingredient_NDB[df_ingredient_NDB.recipe_id == recipe_id_exp]

            print(df_ingredient_NDBi)
            # Retrieve Form Data from User input
            if request.method == 'POST':
                # User has not yet entered an ingredient to sub
                msg_print = ""
                if ingredientSubForm.replacementChoice.data == 'None':
                    # Find options for food replacements
                    try:
                        switch_df, potential_switches = get_single_ingredient_replacement(session, ingredientSubForm, recipe_id_exp)
                        # update session switch options
                        try:
                            session['switch_df_temp'] = switch_df.to_json()
                        except:
                            print("** Error in saving to session")
                        display_bottom = True
                    except:
                        print("GET Ingredient SUB FAILED******")
                        msg_print = "We are sorry, We could not find a good replacment matching your request. Pleasse try again."
                        potential_switches = []
                        display_bottom = False


                    # print(session.keys())
                    # print(pd.read_json(session['switch_df_temp']))
                else:
                    # User entered an ingredient to sub
                    if ingredientSubForm.replacementChoice.data == "DNR":
                        return redirect(url_for('single_ingredient_replacement', recipe_id=recipe_id))

                    # TODO: figure out why saved session switches not saved between page loads
                    # Can load from session if data is saved
                    # if 'switch_df_temp' in session.keys():
                        # switch_df = pd.read_json(session['switch_df_temp'])
                    # else:
                    switch_df, potential_switches = get_single_ingredient_replacement(session, ingredientSubForm, recipe_id_exp)
                    df_ingredient_NDB, df_ingredient_NDBi = switch_out_ingredient(session, recipe_id_exp, ingredientSubForm, switch_df,df_ingredient_NDB, df_ingredient_NDBi)

                    # Save df_ingredient_NDB to session
                    potential_switches = switch_df.potential_switches
                    session['df_ingredient_NDB'] = df_ingredient_NDB.to_json()
                    display_bottom = False
                    msg_print = "We have updated your recipe with the siwtch!"

                print(potential_switches, display_bottom, msg_print)
                # Render the Subsitute Ingredient HTML
                return render_template('subsitute_ingredients.html', form=ingredientSubForm, df_ingredient_NDB=df_ingredient_NDBi[['NDB_NO', 'Description']].values, potential_switches=potential_switches, display_bottom=display_bottom, msg_print=msg_print)

            else:
                # Displays Ingredients User Can Choose to Replace
                return render_template('subsitute_ingredients.html', form=ingredientSubForm, df_ingredient_NDB=df_ingredient_NDBi[['NDB_NO', 'Description']].values, potential_switches=[])
                # return render_template('subsitute_ingredients.html', user_data=pd.read_json(session['data']), df=df, df_list=df_list)
        else:
            # Render the New User SetUp page until they comlete prefernece
            return render_template('userProfile_new.html', title="User Preferneces", user=user)
        return redirect(url_for('index'))


# Force Rerun of Recipe Plan and Display on User Profile Page
@app.route('/rerun_recipe_plan')
def rerun_recipe_plan():
    user = current_user.username
    best_recipe_combo, weekly_diet_amount, user_profile_data, df_ingredient_NDB  = get_recipe_list(session, user)
    # session['df_ingredient_NDB'] = df_ingredient_NDB.to_json()
    return redirect(url_for('recipe_center'))

## Nutrition Center ----------------------------------------------
# Routes and infromation about to Nutrition goals
@app.route('/nutrition_center', methods=['GET', 'POST'])
def nutrition_center():
    if current_user.is_authenticated:
        user = current_user.username
        user_profile_data = pd.read_json(session['data'])
        macros = pd.read_json(session['macros'])
        micros = pd.read_json(session['micros'])

    macros_form = InputMacroNutrientsForm(request.form)
    micros_form = InputMicroNutrientsForm(request.form)
    if request.method == 'POST':
        macros, micros = process_nutrient_edit_form(macros_form.data, micros_form.data, macros, micros)

        # Save micro and Macro edited list for later fram
        session['macros'] = pd.DataFrame(macros).to_json()
        session['micros'] = pd.DataFrame(micros, index=[0]).to_json()

        return render_template("nutrition_center.html", form1=macros_form, form2=micros_form, macros=macros, micros=micros, user_data=user_profile_data)
    else:
        return render_template("nutrition_center.html", form1=macros_form, form2=micros_form, macros=macros, micros=micros, user_data=user_profile_data)


# TODO: sub out placeholder when complete
# Placholder for about page
@app.route('/about_nutrition')
def about_nutrition():
    return render_template('about_nutrition.html')


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


## Other Features
@app.route('/food_network', methods=['GET', 'POST'])
def food_network():
    return render_template('data.html', title="Graph Test")

# Recipe Suggetsion from Pantry Items
@app.route('/pantry_recipe', methods=['GET', 'POST']) #  methods=['GET', 'POST']
def pantry_recipe():

    # pantry Example list to use:
    # 12 large egg, 12 oz mayonnaise, 12 oz BBQ Sauce, 24 oz mustard, 6 skinless chicken breast, 12 salmon burgers, 12 pita, 2 zucchini, 4 onions, 1 pound mushrooms, 12 cups lettuce, 24 beer, 1 whole duck, 4 oranges, 2 potatoes, 2 red peppers, 4 pounds white rice, 48 oz peanut butter, 6 sausage, 4 pounds ham, 1 cauliflower, 6 sticks butter,
    # 12 cups sugar, 12 brown sugar, water, 1 whole lemon, 0.25 cup lemon juice, 10 whole apples, 1 tomato, 0.25 cup Lime juice, 1 bottle rum, 12 egg whites, 1 whole garlic

    if current_user.is_authenticated:
        # Default values for rendering page first time or after clear
        pantry_exists=False
        msg = ''
        has_suggestions=False
        recipe_name_suggestion_list = []
        remove_item = False

        # Get user profile data from session
        user_profile_data = pd.read_json(session['data'])
        user = current_user.username

        # Check if user has a pantry already established
        if 'pantry_items_list' in session.keys():
            pantry_items_list = session['pantry_items_list']
        else:
            pantry_items_list = []

        # Check for existing pantry suggetsions
        if 'pantry_recipe_names' in session.keys():
            pantry_recipe_names = session['pantry_recipe_names']
            if len(pantry_recipe_names)> 0:
                has_suggestions = True
            else:
                has_suggestions = False

        # Get User Forms
        createPantryForm1 = createPantryForm(request.form)
        removePantryItemsForm1 = removePantryItemsForm(request.form)

        # User add pantry data
        if request.method == 'POST':
            print("POST ")
            # Add items to pantry
            if len(pantry_items_list) > 0:
                pantry_exists=True
            else:
                pantry_exists=False
            pantry_items_list = pantry_items_list+[createPantryForm1.pantryItemList.data]

            # separate list of items into individual list items
            pantry_items_list_sep = []
            for item in pantry_items_list:
                pantry_items_list_sep = pantry_items_list_sep+(item.split(","))
            pantry_items_list = pantry_items_list_sep

            # Remove Duplicate and Blank items
            while '' in pantry_items_list:
                pantry_items_list.remove('')
            pantry_items_list = list(set(pantry_items_list))

            # Remove Items From Pantry
            remove_list = []
            if len([removePantryItemsForm1.removePantryItems.data])>0:
                for item in [removePantryItemsForm1.removePantryItems.data]:
                    remove_list = remove_list+(item.split(", "))
                    msg = 'Removed Item From Pantry'
                remove_item = True

            # Save Pantry Updates
            pantry_items_list = list(pantry_items_list)
            try:
                session['pantry_items_list'] = pantry_items_list
            except:
                print("*** ERRROR Saving Pantry list")

        # Get Recipes
        if len(pantry_items_list) > 0:
            pantry_exists=True
            # Run pantry suggestion code here
            try:
                recipe_id_suggestion_list = get_pantry_suggetsions(user_profile_data, pantry_items_list, 5)

                # Process suggestions from input
                recipe_details = get_recipe_details(recipe_id_suggestion_list, pd.read_json(session['data']))
                recipe_name_suggestion_list = []
                recipe_id_suggestion_list = []
                for itr, details in enumerate(recipe_details):
                    recipe_name_suggestion_list.append(recipe_details[itr].get('name'))
                    recipe_id_suggestion_list.append(recipe_details[itr].get('id'))
                has_suggestions = True
                msg = ''
                session['pantry_recipe_names'] = recipe_name_suggestion_list
                session['pantry_recipe_ids'] = recipe_id_suggestion_list
            except:
                has_suggestions = False
                msg = 'We are sorry we did not find a recipe for your pantry. Update pantry and try again'

        else:
            pantry_exists=False

        if remove_item is not False:
            pantry_exists=True
        print(pantry_items_list, recipe_name_suggestion_list, pantry_exists, has_suggestions, msg)
        return render_template('pantry_recipe.html', pantry_items_list=pantry_items_list, recipe_name_suggestion_list=recipe_name_suggestion_list, form1=createPantryForm1, form2=removePantryItemsForm1, pantry_exists=pantry_exists, has_suggestions=has_suggestions, msg=msg)
    else:
        return redirect(url_for('index'))

# Delet Entire Pantry
@app.route('/delete_pantry_items') #  methods=['GET', 'POST']
def delete_pantry_items():
    # "Delet Pantry Items"
    pantry_items_list = session['pantry_items_list']
    pantry_items_list = []
    session['pantry_items_list'] = pantry_items_list
    pantry_recipe_ids = []
    session['pantry_recipe_ids'] = pantry_recipe_ids

    return redirect(url_for('pantry_recipe'))

# Master Run HTML
@app.route('/master_run') #  methods=['GET', 'POST']
def master_run():
    return render_template('master_run.html')
