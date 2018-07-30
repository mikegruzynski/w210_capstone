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
    print(pd.read_json(session['user_meal_plan']))

    df_ingredient_NDB = get_ingredient_NDB_number(session, best_recipe_combo)
    # session['df_ingredient_NDB'] = df_ingredient_NDB.to_json()

    return best_recipe_combo, weekly_diet_amount, user_profile_data, df_ingredient_NDB

# Get ingredient List for Shopping list
def get_recipe_details(best_recipe_combo, user_profile_data):
    profile_init = rootprofile.UserProfile(user_profile_data)
    recipe_init = recipes.Recipes(profile_init)
    print("\n\n******get_recipe_details")
    # get ingredients from the recipe list
    recipe_details = []
    i = 0
    for rec_idx in best_recipe_combo:
        recipe_details.append(recipe_init.recipe_clean[rec_idx])
        # recipe_details = recipe_details.update(rec_idx=recipe_init.recipe_clean[rec_idx])

    print(type(recipe_details), recipe_details)
    return recipe_details


# Get ingredient List for Shopping list
def get_shopping_list(best_recipe_combo, user_profile_data):
    profile_init = rootprofile.UserProfile(user_profile_data)
    recipe_init = recipes.Recipes(profile_init)
    # get ingredients from the recipe list
    ingredient_list = []
    for rec_idx in best_recipe_combo:
        print("\nrec_idx")
        print(recipe_init.recipe_clean[rec_idx])
        ingredient_list = ingredient_list + recipe_init.recipe_clean[rec_idx]['ingredients']

    while '' in ingredient_list:
        ingredient_list.remove('')

    # TODO: aggregate the ingredients to combine recipies and amounts
    print(type(ingredient_list), ingredient_list)
    return(ingredient_list)


def get_ingredient_NDB_number(session, best_recipe_combo):
    # Save ingredients to Session Data
    profile_init = rootprofile.UserProfile(pd.read_json(session['data']))
    recipe_init = recipes.Recipes(profile_init)
    df_ingredient_NDB = pd.DataFrame()
    for recipe_id in best_recipe_combo:
        recipe_data = recipe_init.recipe_list_to_conversion_factor_list(recipe_id)[['Description', 'NDB_NO']]
        df_ingredient_NDBi = pd.DataFrame(recipe_data)
        df_ingredient_NDBi['recipe_id'] = recipe_id
        if df_ingredient_NDB.empty:
            df_ingredient_NDB = df_ingredient_NDBi
        else:
            df_ingredient_NDB = pd.concat([df_ingredient_NDB, df_ingredient_NDBi])

    df_ingredient_NDB = df_ingredient_NDB.reset_index()
    # print(df_ingredient_NDB.recipe_id.unique())

    return(df_ingredient_NDB)


# TODO: Edit single_ingredient_replacement
# TODO: Remove Default call of recipe
def get_single_ingredient_replacement(session, raw_input_return, recipe_id='RECIPE_48743'):
    print("***** SINGLE FOOD REPLACEMENT ******")
    profile_init = rootprofile.UserProfile(pd.read_json(session['data']))
    recipe_init = recipes.Recipes(profile_init)
    research_init = research.Research(profile_init)
    ingredient_list = recipe_init.recipe_clean[recipe_id]['ingredients']
    # Single food replacement based on macros
    # recipe_id = 'RECIPE_48743'
    # print(recipe_init.recipe_list_to_conversion_factor_list(recipe_id)[['Description', 'NDB_NO']])

    # raw_input_return = input("Select items to replace:")
    # raw_input_return = "01116"
    print("HERE")
    print(raw_input_return)
    temp_recipe_dict = {}
    temp_recipe_dict[recipe_id] = recipe_init.recipe_clean[recipe_id].copy()
    print("HERE**************************")
    if raw_input_return:
        # 'Baked'
        # 'Beef'
        # 'Beverages'
        # 'Breakfast_Cereals'
        # 'Cereal_Grains_and_Pasta'
        # 'Dairy_and_Egg'
        # 'Fats_and_Oils'
        # 'Finfish_and_Shellfish'
        # 'Fruits_and_Fruit_Juices'
        # 'Lamb_Veal_and_Game'
        # 'Legumes_and_Legume'
        # 'Nut_and_Seed'
        # 'Pork'
        # 'Poultry'
        # 'Sausages_and_Luncheon_Meats'
        # 'Soups_Sauces_and_Gravies'
        # 'Spices_and_Herbs'
        # 'Sweets'
        # 'Vegetables_and_Vegetable'

        # tag_list = research_init.macro_space_distance_top_n(3, raw_input_return, ['Finfish_and_Shellfish'])
        tag_list = research_init.macro_space_distance_top_n(3, raw_input_return, ['Finfish_and_Shellfish'])
        print("tag_list", tag_list)
        new_recipe_dict = recipe_init.recipe_alternitive_create(raw_input_return, tag_list, temp_recipe_dict)
        print("new_recipe_dict", new_recipe_dict)
        temp = recipe_init.recipe_list_to_conversion_factor_list(recipe_id)

        df_list = []
        name_list = []
        for recipe in new_recipe_dict.keys():
            temp_recipe_df = recipe_init.recipe_list_to_conversion_factor_list(recipe, dict=new_recipe_dict)
            df_list.append(temp_recipe_df)
            name_list.append(new_recipe_dict[recipe]['name'])

        # visualizations.Plots(df_list, profile_init).bar_plot_recipe(name_list, 'test_replacement_barplot')
        # visualizations.Plots(df_list, profile_init).radar_plot_recipe(name_list, 'test_replacement_radar_plot')
        print("df_list", df_list)
        print("\n")
        print("df", df)
        # TODO: Figure out what to return
        # TODO: Replace the ingredients in the session data
        # TODO: Edit the REcipe with the replacemnt ingredient
    return ingredient_list # df, df_list


# Single food Subsitution
# def single_food_subsitution():
# TODO
