from app import app, db
from flask import render_template, flash, redirect, url_for, session, request
from flask_login import current_user, login_user, logout_user
from app.forms import LoginForm, RegistrationForm, UserPreferenceForm
from app.models import *
from app.user_profile_support.get_user_nutrients import *
from app.user_profile_support.get_userPreference_Answers import *
from app.user_profile_support.ingredientSubsitutions import *
from app.user_profile_support.get_recipe_center_data import *
from app.user_profile_support.rootseller import macronutrients
from app.user_profile_support.rootseller.generate_plotly_plots import *
# from app.user_profile_support.rootseller import micronutrients
# import math, json
# import plotly.plotly as py
# import plotly.graph_objs as go
# from plotly.utils import PlotlyJSONEncoder
# import numpy as np
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
    if 'pantry_Suggestions ids' in session.keys():
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
        # Check if user is New or Returning
        print(session.keys())
        if 'data' in session.keys():
            data = pd.read_json(session['data'])
            is_new_user = False
            user = data.firstname.values[0]
        else:
            is_new_user = True
            user = current_user.username

        return render_template('survey.html', title='Preferences', user=user, is_new_user=is_new_user)
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

            # Check to make sure recipes are not in the ignore list
            ignore_list = get_user_ignore_responses(session, user)
            while any(np.intersect1d(ignore_list, user_meal_plan.recipe_id)):
                best_recipe_combo, weekly_diet_amount, user_profile_data, df_ingredient_NDB = get_recipe_list(session, user)
                user_meal_plan = pd.read_json(session['user_meal_plan'])

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
            # user_meal_plan = return_user_meal_plan(session, user_profile_data, user)

            # Create Radar, Bar Plots for recipe recommendations
            df, df_list, df_summed_list, profile_init, name_list = create_recipe_rec_df(session, user_meal_plan)
            ids, graphJSON, data_meal_plan_radar_macro, layout_meal_plan_radar_macro, data_meal_plan_radar_micro, layout_meal_plan_radar_micro = full_recipe_rec_plots(df, df_list, df_summed_list, profile_init, session, name_list)

            # Get Forms for Processing Data Requests -----------------------------
            # Get Names of Recipe plan
            recipe_names = user_meal_plan.recipe_name.values
            recipe_names_choices = [(i, x) for i, x in enumerate(recipe_names)]

            # Form for customizing Serving Sizes
            # scaleRecipeForm1 = scaleRecipeForm(request.form)
            scaleRecipeForm1 = scaleRecipeForm(request.form)
            scaleRecipeForm1.customizeRecipeName.choices = recipe_names_choices

            # Get IgnoreRecipeForm and Populate Options for Checkboxes
            ignoreRecipeForm = IgnoreRecipeForm(request.form)
            # Add Choices for ignoreing Recipes to Forms
            ignoreRecipeForm.ignore_list.choices = recipe_names_choices

            # Form for Choosing the Recipe to choose ingredients to Subsitute
            recipeNameIdForm = ChooseRecipeToSubIngredients(request.form)
            recipeNameIdForm.recipe_name.choices = recipe_names_choices

            if request.method == 'POST':
                # Process Form Data
                # Ingredient Replacment Request
                if recipeNameIdForm.recipe_name.data is not None:
                    t = user_meal_plan.iloc[int(recipeNameIdForm.recipe_name.data)]
                    recipe_name = t.recipe_name
                    best_recipe_combo = user_meal_plan.recipe_id
                    recipe_details = get_recipe_details(best_recipe_combo, user_profile_data)
                    recipe_id = get_recipe_id_from_name(recipe_name, recipe_details)
                    print(recipe_details)
                    return redirect(url_for('single_ingredient_replacement', recipe_id=recipe_id))

                if scaleRecipeForm1.customizeRecipeName.data is not None:
                    # Get recipe Name
                    t = user_meal_plan.iloc[int(scaleRecipeForm1.customizeRecipeName.data)]
                    recipe_id = t.recipe_id
                    recipe_details = get_recipe_details(user_meal_plan.recipe_id, user_profile_data)
                    return redirect(url_for('customize_serving_size', recipe_id=recipe_id))

                # Ignore ingredient request
                if ignoreRecipeForm.ignore_list.data is not None:
                    print("**TODO: Clear box when submitted")
                    # TODO: clear input box after submit
                    process_ignore_form(session, ignoreRecipeForm)
                    # Render the Users Profile Page
                    update_text = 'Sorry you did not like the recipes! You will not see it again. Regenerate your recipe plan for new suggestions'

                # Ignore ingredient request
                print("**TODO: Clear box when submitted")
                # TODO: clear input box after submit
                return render_template('recipe_recommendation.html', user_data=user_profile_data, user_meal_plan=user_meal_plan, ignore_form=ignoreRecipeForm, form2=recipeNameIdForm,
                                update_text=update_text, ids=ids, graphJSON=graphJSON,
                                   radar_data_macro=data_meal_plan_radar_macro,
                                   radar_layout_macro=layout_meal_plan_radar_macro,
                                    radar_data_micro=data_meal_plan_radar_micro,
                                       radar_layout_micro=layout_meal_plan_radar_micro,
                                       scaleRecipeForm = scaleRecipeForm1
                                       )
            else:
                return render_template('recipe_recommendation.html', user_data=user_profile_data, user_meal_plan=user_meal_plan, ignore_form=ignoreRecipeForm, form2=recipeNameIdForm, update_text=update_text,
                ids=ids, graphJSON=graphJSON, radar_data_macro=data_meal_plan_radar_macro,
                                       radar_layout_macro=layout_meal_plan_radar_macro,
                                           radar_data_micro=data_meal_plan_radar_micro,
                                           radar_layout_micro=layout_meal_plan_radar_micro,
                                           scaleRecipeForm = scaleRecipeForm1)
        else:
            # Render the New User SetUp page until they comlete prefernece
            return render_template('userProfile_existing.html', user_data=user_profile_data, macros=macros, micros=micros)
        return redirect(url_for('index'))


# Customize Serving Size of Recipe
# @app.route('/customize_serving_size/<recipe_id>')
# def customize_serving_size(recipe_id):
#     print("Customize Recipe")
#     print(recipe_id)
#     user = current_user.username
#     if pd.read_json(session['data']) is not False:
#         user_meal_plan = pd.read_json(session['user_meal_plan'])
#
#         return render_template('customize_serving_size.html', recipe_id=recipe_id)
#     return redirect(url_for('index'))

# Customize Serving Size of Recipe
@app.route('/customize_serving_size/<recipe_id>')
def customize_serving_size(recipe_id):
    print("Customize Recipe")
    print(recipe_id)
    user = current_user.username
    if pd.read_json(session['data']) is not False:
        user_meal_plan = pd.read_json(session['user_meal_plan'])
        user_profile_data = pd.read_json(session['data'])
        profile_init = rootprofile.UserProfile(user_profile_data)
        recipe_init = recipes.Recipes(profile_init)
        init_macro = macronutrients.Macronutrients(user_profile_data)

        temp_recipe_df = recipe_init.recipe_list_to_conversion_factor_list(recipe_id)
        temp_recipe_df = temp_recipe_df[~temp_recipe_df.isin(profile_init.micro_list)].reset_index(drop=True)

        # multiplier_normalizer = profile_init.profile_macro_filtered_df['calories'].get_values()[0] / 3.0
        # multiplier_normalizer = multiplier_normalizer / temp_recipe_df['Energy (kcal)'].sum()
        # for column in profile_init.macro_list + ['conversion_factor']:
        #     temp_recipe_df[column] = temp_recipe_df[column] * multiplier_normalizer

        new_columns = init_macro.convert_labels_to_pretty_labels(temp_recipe_df.columns)
        temp_recipe_df.columns = new_columns
        temp_recipe_df_original = init_macro.add_unsaturated_fat_columns(temp_recipe_df)
        temp_recipe_df_original = temp_recipe_df_original[~temp_recipe_df_original.isin(profile_init.micro_list)].reset_index(drop=True)

        num_generations = 30
        amount_per_population = 40
        amount_parents_mating = 20
        GA_init = models.GA(macro_list=profile_init.macro_label_list)
        daily_diet_amount = (GA_init.user_df[GA_init.macro_labels] / 3.0)

        df_AMGA_single = GA_init.AMGA_individual_recipe(num_generations, temp_recipe_df_original, amount_per_population,
                                           amount_parents_mating, daily_diet_amount)

        temp_recipe_df_AMGA = temp_recipe_df_original.copy()
        temp_recipe_df_AMGA = temp_recipe_df_AMGA[~temp_recipe_df_AMGA.isin(profile_init.micro_list)].reset_index(drop=True)

        new_scale_list = []
        for index in temp_recipe_df_AMGA.index:
            scale_factor = df_AMGA_single.loc[index, 'new_conversion_factor'] / df_AMGA_single.loc[index, 'original_conversion_factor']
            new_scale_list.append(scale_factor)
            for column in profile_init.macro_label_list:
                temp_recipe_df_AMGA.loc[index, column] = temp_recipe_df_AMGA.loc[index, column] * scale_factor


        trace_radar_macro_list = []
        r_macro = temp_recipe_df_AMGA[profile_init.macro_label_list].sum() / daily_diet_amount[profile_init.macro_label_list]
        r_macro = r_macro[profile_init.macro_label_list].values.tolist()[0]
        theta_macro = profile_init.macro_label_list.copy()
        # theta_macro.append(theta_macro[0])
        temp_trace_radar_macro = dict(
            type='scatterpolar',
            r=r_macro,
            theta=theta_macro,
            fill='toself',
            opacity=0.5,
            text=temp_recipe_df_AMGA[profile_init.macro_label_list].values.tolist()[0],
            hoverInfo='text',
            name="Optimized Personal Serving Recipe",
            marker=dict(color='blue',
                        size=10)
            )


        trace_radar_macro_list.append(temp_trace_radar_macro)
        r_macro = temp_recipe_df_original[profile_init.macro_label_list].sum() / daily_diet_amount[profile_init.macro_label_list]
        r_macro = r_macro[profile_init.macro_label_list].values.tolist()[0]
        theta_macro = profile_init.macro_label_list.copy()
        # theta_macro.append(theta_macro[0])
        temp_trace_radar_macro = dict(
            type='scatterpolar',
            r=r_macro,
            theta=theta_macro,
            fill='toself',
            opacity=0.5,
            text=temp_recipe_df_original[profile_init.macro_label_list].values.tolist()[0],
            hoverInfo='text',
            name="Original Recipe",
            marker=dict(color='red',
                        size=10)
            )
        recipe_temp_df_normalized = temp_recipe_df_AMGA[profile_init.macro_label_list] / temp_recipe_df_AMGA[profile_init.macro_label_list].sum()
        recipe_temp_df_normalized = recipe_temp_df_normalized[profile_init.macro_label_list]
        master_stack_list = []

        # df_AMGA_single_col_bar_stacked =
        for index in temp_recipe_df_AMGA.index:
            temp = dict(
                x=profile_init.macro_label_list.copy(),
                y=recipe_temp_df_normalized.loc[index, profile_init.macro_label_list].values.tolist(),
                type='bar',
                name=temp_recipe_df_AMGA.loc[index, 'Description'],
                text=temp_recipe_df_AMGA.loc[index, profile_init.macro_label_list].values.tolist(),
                hoverInfo='text')
            master_stack_list.append(temp)


        trace_radar_macro_list.append(temp_trace_radar_macro)
        layout_meal_plan_radar_macro = dict(polar=dict(radialaxis=dict(visible=True)))
        layout_single_stacked_bar = dict(barmode='stack')
        ingredients = recipe_init.recipe_clean[recipe_id]['ingredients']
        instructions = recipe_init.recipe_clean[recipe_id]['instructions']

        new_ingredient_list = []
        for cf_itr in range(len(new_scale_list)):
            if ingredients[cf_itr]:
                ingredients_split = ingredients[cf_itr].split(" ")
                amount = float(ingredients_split[0])
                amount = amount * new_scale_list[cf_itr]
                del ingredients_split[0]
                ingredients_split = [str(round(amount, 2))] + ingredients_split
                ingredient_new = " ".join(ingredients_split)
                new_ingredient_list.append(ingredient_new)
            else:
                new_ingredient_list.append("")

        df_show = pd.DataFrame({'Ingredients': new_ingredient_list})

        return render_template('customize_serving_size.html', recipe_id=recipe_id,
                               radar_data_macro=trace_radar_macro_list, radar_layout_macro=layout_meal_plan_radar_macro,
                               df_show=df_show.to_html(index=False), instructions=instructions,
                               bar_data_macro=master_stack_list, bar_layout_macro=layout_single_stacked_bar)
        # return render_template('customize_serving_size.html', recipe_id=recipe_id)
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
            recipe_id_exp = "RECIPE_"+str(recipe_id) # Recipe User is choosing to Edit
            recipe_name = user_meal_plan.recipe_name[user_meal_plan.recipe_id == recipe_id_exp].values[0]

            # Get input Form from models for html
            # Get Ingredients from Recipe as options to replace
            df_ingredient_NDB = get_ingredient_NDB_number(session, best_recipe_combo)
            session['df_ingredient_NDB'] = df_ingredient_NDB.to_json()
            df_ingredient_NDBi = df_ingredient_NDB[df_ingredient_NDB.recipe_id == recipe_id_exp]


            ingredient_choice_list = []
            for i, desc in enumerate(df_ingredient_NDBi[['Description']].values):
                ingredient_choice_list = ingredient_choice_list + [(i, desc[0])]

            # Initialize Form and Choices
            food_type_choice_list = [('1','Baked'), ('2','Beef'),
            ('3','Beverages'), ('4','Breakfast_Cereals'), ('5','Cereal_Grains_and_Pasta'),
            ('6','Dairy_and_Egg'), ('7','Fats_and_Oils'), ('8','Finfish_and_Shellfish'),
            ('9','Fruits_and_Fruit_Juices'), ('10','Lamb_Veal_and_Game'), ('11','Legumes_and_Legume'),
            ('12','Nut_and_Seed'), ('13','Pork'), ('14','Poultry'), ('15','Sausages_and_Luncheon_Meats'),
            ('16','Soups_Sauces_and_Gravies'), ('17','Spices_and_Herbs'),
            ('18','Sweets'), ('19','Vegetables_and_Vegetable')]


            # Call Forms
            ingredientSubForm = IngredientSubForm(request.form)
            ingredientSubForm.ingredientSub.choices = ingredient_choice_list
            ingredientSubForm.foodType.choices = food_type_choice_list
            sub_choices = [(0, 'Subsitute 1'), (1, 'Subsitute 2'), (2, 'Subsitute 3'), (3, 'Do Not Replace')]
            ingredientSubForm.replacementChoice.choices = sub_choices
            # ingredientSubForm = IngredientSubForm.edit_food_types(food_types_list=food_type_choice_list)

            # Retrieve Form Data from User input
            if request.method == 'POST':
                # User has not yet entered an ingredient to sub
                msg_print = ""
                if ingredientSubForm.replacementChoice.data is None:
                    # Get nbd_no
                    nbd_no = df_ingredient_NDBi.iloc[int(ingredientSubForm.ingredientSub.data)].NDB_NO
                    # Find options for food replacements

                    try:
                        switch_df, potential_switches = get_single_ingredient_replacement(session, ingredientSubForm, recipe_id_exp, nbd_no)
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

                    # Check if Subsitute Choices exist. If they do use those choices.
                    # else use default sub_choices
                    if len(potential_switches)>0:
                        sub_choices = []
                        for i, switch in enumerate(potential_switches):
                            sub_choices = sub_choices + [(i, switch)]
                        sub_choices = sub_choices+[(3,'Do Not Replace')]
                    else:
                        sub_choices = [(0, 'Subsitute 1'), (1, 'Subsitute 2'), (2, 'Subsitute 3'), (3, 'Do Not Replace')]

                    ingredientSubForm.replacementChoice.choices = sub_choices
                else:
                    # User entered an ingredient to sub
                    if ingredientSubForm.replacementChoice.data == 3:
                        return redirect(url_for('single_ingredient_replacement', recipe_id=recipe_id))

                    nbd_no = df_ingredient_NDBi.iloc[int(ingredientSubForm.ingredientSub.data)].NDB_NO

                    switch_df, potential_switches = get_single_ingredient_replacement(session, ingredientSubForm, recipe_id_exp, nbd_no)
                    df_ingredient_NDB, df_ingredient_NDBi = switch_out_ingredient(session, recipe_id_exp, ingredientSubForm, switch_df, df_ingredient_NDB, df_ingredient_NDBi, old_nbd_no=nbd_no)

                    # Save df_ingredient_NDB to session
                    potential_switches = switch_df.potential_switches
                    session['df_ingredient_NDB'] = df_ingredient_NDB.to_json()
                    display_bottom = False
                    msg_print = "We have updated your recipe with the siwtch!"

                    # update the ingredients form
                    ingredient_choice_list = []
                    for i, desc in enumerate(df_ingredient_NDBi[['Description']].values):
                        ingredient_choice_list = ingredient_choice_list + [(i, desc[0])]
                    ingredientSubForm.ingredientSub.choices = ingredient_choice_list

                print(df_ingredient_NDBi[['NDB_NO', 'Description']].values)
                # Render the Subsitute Ingredient HTML
                return render_template('subsitute_ingredients.html', form=ingredientSubForm, df_ingredient_NDB=df_ingredient_NDBi[['NDB_NO', 'Description']].values,
                potential_switches=potential_switches, display_bottom=display_bottom, msg_print=msg_print, recipe_name=recipe_name)

            else:
                # Displays Ingredients User Can Choose to Replace
                return render_template('subsitute_ingredients.html', form=ingredientSubForm, df_ingredient_NDB=df_ingredient_NDBi[['NDB_NO', 'Description']].values,
                potential_switches=[], display_bottom=False, recipe_name=recipe_name)
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
        user_profile_data = pd.read_json(session['data'])
        if user_profile_data is not False:
            user = current_user.username
            # Get Ingredient List to Create a Shopping List
            user_meal_plan = return_user_meal_plan(session, user_profile_data, user)

            #// START: initialize for df creation to plot bar/radar plots
            profile_init = rootprofile.UserProfile(user_profile_data)
            recipe_init = recipes.Recipes(profile_init)
            # recipe_init = recipes.Recipes(profile_init)
            list_keys = user_meal_plan['recipe_id'].get_values()
            recipe_itr = 0
            weight_lb_list = []
            amount_recipe_list = []
            unit_recipe_list = []
            df_list = []
            for recipe in list_keys:
                # print("*******************************", "Recipe Itr: ", recipe_itr, "Out of: ", len(list_keys) - 1, recipe)
                # try:
                temp_recipe_df = recipe_init.recipe_list_to_conversion_factor_list(recipe)
                temp_recipe_df = temp_recipe_df.reset_index(drop=True)
                multiplier_normalizer = profile_init.profile_macro_filtered_df['calories'].get_values()[0] / 3.0
                multiplier_normalizer = multiplier_normalizer / temp_recipe_df['Energy (kcal)'].sum()
                temp_recipe_df['conversion_factor'] = temp_recipe_df['conversion_factor'] * multiplier_normalizer
                temp_recipe_df = temp_recipe_df[["NDB_NO", "Description", 'conversion_factor']]
                df_list.append(temp_recipe_df)

                for index in temp_recipe_df.index:
                    try:
                        temp = recipe_init.nutrition_init.NDB_NO_lookup(temp_recipe_df.loc[index, 'NDB_NO'],
                                                                   filter_list=['Weight(g)', 'Measure']).get_values()[0]
                        temp = temp.tolist()
                        weight = float(temp[0]) * float(temp_recipe_df.loc[index, 'conversion_factor']) * 0.00220462
                        temp_split = temp[1].split(" ")
                        amount_recipe = float(temp_split[0]) * float(temp_recipe_df.loc[index, 'conversion_factor'])
                        del temp_split[0]
                        unit_recipe = " ".join(temp_split)

                        weight_lb_list.append(weight)
                        amount_recipe_list.append(amount_recipe)
                        unit_recipe_list.append(unit_recipe)

                    except:
                        weight_lb_list.append(0.0)
                        amount_recipe_list.append(0.0)
                        unit_recipe_list.append(0.0)

            master_df = pd.concat(df_list)
            se = pd.Series(weight_lb_list)
            master_df['Weight (lb)'] = se.values
            se2 = pd.Series(amount_recipe_list)
            master_df['Amount'] = se2.values
            se3 = pd.Series(unit_recipe_list)
            master_df['Unit'] = se3.values
            df_sum = master_df[['NDB_NO', 'Weight (lb)', 'Amount', 'Unit', 'Description']].groupby(['NDB_NO', 'Unit', 'Description']).sum().reset_index()
            df_final = df_sum.merge(master_df[['NDB_NO', 'Amount']])
            df_final['Unit Total'] = df_final[['Amount', 'Unit']].apply(lambda x: '{} {}'.format(math.ceil(x[0]), x[1]), axis=1)
            df_final['Weight (lb)'] = round(df_final['Weight (lb)'], 3)
            del df_final['Amount']
            del df_final['Unit']
            del df_final['NDB_NO']
            df_final = df_final[round(df_final['Weight (lb)'], 3) != round(0, 3)]
            # ingredient_list = list(set(df_final.Description))
            df_show = df_final[['Unit Total', 'Description']]
            return render_template('shopping_list.html', df_show=df_show.to_html(index=False, justify='left'), user_data=user_profile_data)
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
        return render_template('pantry_recipe.html', pantry_items_list=pantry_items_list,
        recipe_name_suggestion_list=recipe_name_suggestion_list, form1=createPantryForm1,
        form2=removePantryItemsForm1, pantry_exists=pantry_exists, has_suggestions=has_suggestions, msg=msg)
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


@app.route('/sample_profile')
def sample_profile():
   return render_template('sample_profile.html')


@app.route('/about_the_models')
def about_the_models():
   return render_template('about_the_models.html')


# # Plotly Test
# @app.route('/plotly_test')
# def plotly_test():
#     import plotly.plotly as py
#     import plotly.graph_objs as go
#     import json
#     from plotly.utils import PlotlyJSONEncoder
#
#     trace1 = go.Bar(
#         x=['giraffes', 'orangutans', 'monkeys'],
#         y=[20, 14, 23],
#         name='SF Zoo'
#     )
#     trace2 = go.Bar(
#         x=['giraffes', 'orangutans', 'monkeys'],
#         y=[12, 18, 29],
#         name='LA Zoo'
#     )
#
#     data = [trace1, trace2]
#     layout = go.Layout(
#         barmode='stack'
#     )
#
#     graphs = [dict(data=data, layout=layout)]
#     ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]
#
#
#     graphJSON = json.dumps(graphs, cls=PlotlyJSONEncoder)
#     return render_template('index.html',
#                            ids=ids,
#                            graphJSON=graphJSON)
