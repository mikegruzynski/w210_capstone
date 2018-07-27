# Code to support Ingredient subsitions
# Mostly from master_run in rootsellar folder
recipe_itr = 0
best_recipe_combo = []
from flask import session
from app.user_profile_support.rootseller import rootprofile
from app.user_profile_support.rootseller import recipes, research
from app.user_profile_support.rootseller import models
from app.user_profile_support.rootseller.recipes import Recipes
from app.user_profile_support.rootseller import visualizations
from app.user_profile_support.get_userPreference_Answers import get_user_ignore_responses
import pandas as pd
import numpy as np

def recipe_visuals(df_list, df, profile_init, name_list):
    visualizations.Plots(df_list, df, profile_init).radar_plot_recipe(name_list)
    visualizations.Plots(df_list, df, profile_init).stacked_barplot(0, name_list)
    visualizations.Plots(df_list, df, profile_init).bar_plot_recipe(name_list)


def get_recipe_list(session, user):
    user_profile_data = pd.read_json(session['data'])

    # Run Recipe Recomendation Alg
    profile_init = rootprofile.UserProfile(user_profile_data)
    recipe_init = recipes.Recipes(profile_init)

    # Check for any recipes to ignore
    ignore_list = get_user_ignore_responses(user_profile_data, user)

    # number of meal preferences
    if 'meals_per_week' not in user_profile_data.keys():
        meals_per_week = 6 # Default
    elif user_profile_data.meals_per_week.values[0] == '':
        meals_per_week = 6 # Default - User did not specify in survey
    else:
        meals_per_week = int(user_profile_data.meals_per_week.values[0])

    # Algroithm initiation settings
    num_generations = 10
    amount_per_population = 30
    amount_parents_mating = 10
    # Run GA Recipe/Meal Plan Optimization
    GA = models.GA()
    label_of_weights = GA.labels
    weekly_diet_amount = (GA.user_df[GA.macro_labels] / 3.0) * meals_per_week
    best_recipe_combo, weekly_diet_amount = GA.AMGA(num_generations, meals_per_week, amount_per_population, amount_parents_mating, weekly_diet_amount, ignore_list)
    # user_profile_data['list_keys'] = [best_recipe_combo]
    # user_profile_data.list_keys = best_recipe_combo
    user_profile_data['plan_exists'] = True
    recipe_names = []
    for rec_idx in best_recipe_combo:
        recipe_names.append(recipe_init.recipe_clean[rec_idx]['name'])
    # user_profile_data.recipe_names = recipe_names
    # user_profile_data['recipe_names'] = [recipe_names]

    user_meal_plan = pd.DataFrame(data={'recipe_id':best_recipe_combo, 'recipe_name':recipe_names})
    session['user_meal_plan'] = user_meal_plan.to_json()
    return best_recipe_combo, weekly_diet_amount, user_profile_data

# Get ingredient List for Shopping list
def get_shopping_list(best_recipe_combo, user_profile_data):
    profile_init = rootprofile.UserProfile(user_profile_data)
    recipe_init = recipes.Recipes(profile_init)
    # get ingredients from the recipe list
    ingredient_list = []
    for rec_idx in best_recipe_combo:
        ingredient_list = ingredient_list + recipe_init.recipe_clean[rec_idx]['ingredients']

    while '' in ingredient_list:
        ingredient_list.remove('')

    # TODO: aggregate the ingredients to combine recipies and amounts

    return(ingredient_list)

# TODO:
def run_master_ingredient_sub(user_profile_data):
    profile_init = rootprofile.UserProfile(user_profile_data)
    recipe_init = recipes.Recipes(profile_init)
    research_init = research.Research(profile_init)

    # Run Subsitution option for Ingredients
    recipe_itr = 0
    df_list = []
    df_summed_list = []
    recipe_id_list = []
    name_list = []

    if user_profile_data.plan_exists == False:
    # If no recipes exist for user create a meal plan
        best_recipe_combo, weekly_diet_amount, user_profile_data, user_meal_plan = get_recipe_list(user_profile_data, recipe_init)

    for recipe in user_meal_plan.recipe_id:
        temp_recipe_df = recipe_init.recipe_list_to_conversion_factor_list(recipe)
        df_list.append(temp_recipe_df)
        df_summed_list.append(temp_recipe_df.loc[:, profile_init.macro_list + profile_init.micro_list].sum().to_frame())
        name_list.append(recipe_init.recipe_clean[recipe]['name'])
        recipe_id_list.append(recipe)
        recipe_itr += 1

    # SMASH Files together for optimization mapp
    df = pd.concat(df_summed_list, axis=1)
    df = df.T.reset_index(drop=True)
    se = pd.Series(name_list)
    df['recipe_name'] = se.values
    se2 = pd.Series(recipe_id_list)
    df['recipe_id'] = se2.values

    # Create Recipe Visuals for Display
    recipe_visuals(df_list, df, profile_init, name_list)

    return df, df_list


# Single food Subsitution
# def single_food_subsitution():
# TODO
