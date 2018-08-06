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
import itertools

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

    df_ingredient_NDB = get_ingredient_NDB_number(session, best_recipe_combo)
    # session['df_ingredient_NDB'] = df_ingredient_NDB.to_json()

    return best_recipe_combo, weekly_diet_amount, user_profile_data, df_ingredient_NDB

# Get ingredient List for Shopping list
def get_recipe_details(best_recipe_combo, user_profile_data):
    profile_init = rootprofile.UserProfile(user_profile_data)
    recipe_init = recipes.Recipes(profile_init)
    # get ingredients from the recipe list
    recipe_details = []
    i = 0
    for rec_idx in best_recipe_combo:
        recipe_details.append(recipe_init.recipe_clean[rec_idx])
        # recipe_details = recipe_details.update(rec_idx=recipe_init.recipe_clean[rec_idx])

    return recipe_details

# Lookup Recipe ID from Name
def get_recipe_id_from_name(recipe_name, recipe_details):
    for itr, details in enumerate(recipe_details):
        if recipe_details[itr].get('name') == recipe_name:
            recipe_id = recipe_details[itr].get('id')
            break
    return recipe_id

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
    print("***TODO: aggregate the ingredients to combine recipies and amounts")
    # print(type(ingredient_list), ingredient_list)
    return(ingredient_list)


def get_ingredient_NDB_number(session, best_recipe_combo):
    # Returns Ingredits in recipes to dataframe
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


# Replaces 1 ingredient in a recipe as user chooses
def get_single_ingredient_replacement(session, ingredientSubForm, recipe_id):
    # Single food replacement based on macros

    # Get intial information on user
    profile_init = rootprofile.UserProfile(pd.read_json(session['data']))
    recipe_init = recipes.Recipes(profile_init)
    research_init = research.Research(profile_init)
    ingredient_list = recipe_init.recipe_clean[recipe_id]['ingredients']

    # temp_recipe_dict = {}
    # temp_recipe_dict[recipe_id] = recipe_init.recipe_clean[recipe_id].copy()
    if len(ingredientSubForm.ingredientSub.data) > 0:
        replacement_key_dict = {1:  'Baked',
                                2:  'Beef',
                                3:  'Beverages',
                                4:  'Breakfast_Cereals',
                                5:  'Cereal_Grains_and_Pasta',
                                6:  'Dairy_and_Egg',
                                7:  'Fats_and_Oils',
                                8:  'Finfish_and_Shellfish',
                                9:  'Fruits_and_Fruit_Juices',
                                10: 'Lamb_Veal_and_Game',
                                11: 'Legumes_and_Legume',
                                12: 'Nut_and_Seed',
                                13: 'Pork',
                                14: 'Poultry',
                                15: 'Sausages_and_Luncheon_Meats',
                                16: 'Soups_Sauces_and_Gravies',
                                17: 'Spices_and_Herbs',
                                18: 'Sweets',
                                19: 'Vegetables_and_Vegetable'}


        # split_raw_return = raw_input_return.split(",")
        # "05097":8,"44005":7
        # TODO: improve to allow user to input multiple replacements
        # master_tag_list = []
        # replace_list = []
        # for replacement_ndb_tag in range(len(ingredientSubForm.ingredientSub.data)):
        # replacement_ndb_tag = replacement.split(":")[0].lstrip(" ")
        # replacement_category_key = int(replacement.split(":")[-1].strip("'").strip('"'))
        replacement_ndb_tag = ingredientSubForm.ingredientSub.data
        replacement_category_key = ingredientSubForm.foodType.data

        # Taglist = suggested replacemnt food indicies
        tag_list, potential_switches = research_init.macro_space_distance_top_n(4, replacement_ndb_tag, [replacement_key_dict[int(replacement_category_key)]])

        # Verify one of top three option is not the same as input
        for i, tag in enumerate(tag_list):
            if tag.strip('"') == replacement_ndb_tag:
                tag_list.remove(tag)
                potential_switches.remove(potential_switches[i])
        switch_df = pd.DataFrame(data={'tags':tag_list[:3], "potential_switches":potential_switches[:3]})
        session['potential_switches'] = potential_switches
        # DO following process to get visuals
        # Split User input into the item to replace and type, format: ['"44005":7']
        # master_tag_list = []
        # replace_list = []
        # new_recipe_dict = recipe_init.recipe_alternitive_create(replacement_ndb_tag, tag_list, temp_recipe_dict)
        # replace_list.append(replacement_ndb_tag)
        # master_tag_list.append(tag_list)

        # # Create an iterable list. Change Masetr tage list from:
        # # master_tag_list =  [['"04042"', '"04618"', '"04545"']] to
        # # iterable_list =  [('"04042"',), ('"04618"',), ('"04545"',)]
        # iterable_list = list(itertools.product(*master_tag_list))
        # new_recipe_dict = recipe_init.recipe_alternitive_iter_create(replace_list, iterable_list, temp_recipe_dict)
        #
        # print("\n\nCreated iterable list ")
        # print("new_recipe_dict", new_recipe_dict, "iterable_list", iterable_list)
        # temp = recipe_init.recipe_list_to_conversion_factor_list(recipe_id)
        # df_list = []
        # name_list = []
        # for recipe in new_recipe_dict.keys():
        #     temp_recipe_df = recipe_init.recipe_list_to_conversion_factor_list(recipe, dict=new_recipe_dict)
        #     df_list.append(temp_recipe_df)
        #     name_list.append(new_recipe_dict[recipe]['name'])
        # print('*____ Visuals ___*')
        # print("df_list", df_list)
        # print("profile_init", profile_init)
        # print('name_list', name_list)
        # # visualizations.Plots(df_list, profile_init).bar_plot_recipe(name_list, 'test_replacement_barplot')
        # print("visual 1")
        # # visualizations.Plots(df_list, profile_init).radar_plot_recipe(name_list, 'test_replacement_radar_plot')
        # print("visual 2")
        return switch_df, potential_switches[:3]


# Return Choices for Ingredien Sub
def get_potential_switch_choices():
    # print(session.keys())
    # print(session['potential_switches'])
    choices = ['Subsitute 1', 'Subsitute 2', 'Subsitute 3']
    # choices = session['potential_switches']
    return(choices)

# Switch the ingrediet out for the user selected ingredient
# For Single Ingredient Subsitution
def switch_out_ingredient(session, recipe_id, ingredientSubForm, switch_df, df_ingredient_NDB, df_ingredient_NDBi):
    # Get User information details
    user_meal_plan = pd.read_json(session['user_meal_plan'])
    best_recipe_combo = user_meal_plan.recipe_id
    recipe_details = get_recipe_details(best_recipe_combo, pd.read_json(session['data']))

    # Finds Recipe Details for recipe we are interested iin
    rid = recipe_id.strip('RECIPE_')
    for itr, details in enumerate(recipe_details):
        if recipe_details[itr].get('id') == rid:
            recipe_itr = itr
            break

    # Save new tag and ingredient information as varibales
    new_NBD_tag = switch_df.tags[int(ingredientSubForm.replacementChoice.data)-1]
    new_ingredient = switch_df.potential_switches[int(ingredientSubForm.replacementChoice.data)-1]
    curr_recipe = recipe_details[recipe_itr]

    # Get Ingredients and tags of Current Recipe
    NDB_no_tags = curr_recipe.get('NDB_NO_tags')
    ingredients = curr_recipe.get('ingredients')

    # Update Values in current recipe to reflect change
    # for i, tag in enumerate(NDB_no_tags):
    for i, tag in enumerate(df_ingredient_NDBi.NDB_NO):
        if tag.strip('"') == ingredientSubForm.ingredientSub.data:
            NDB_no_tags.remove(tag)
            NDB_no_tags.append(new_NBD_tag)
            index_val = df_ingredient_NDBi.NDB_NO.index[i]
            df_ingredient_NDBi.NDB_NO[index_val] = new_NBD_tag
            df_ingredient_NDBi.Description[index_val] = new_ingredient

    # curr_recipe["NDB_NO_tags"] = df_ingredient_NDBi.NDB_NO.values
    # curr_recipe["ingredients"] = df_ingredient_NDBi.Description.values

    # Replace With Updates: Save the Ingredient Updates to profileself.
    df_ingredient_NDB_mi = df_ingredient_NDB[df_ingredient_NDB.recipe_id != recipe_id]
    df_ingredient_NDB = pd.concat([df_ingredient_NDB_mi, df_ingredient_NDBi])
    if 'level_0' in df_ingredient_NDB.columns:
        df_ingredient_NDB.drop(columns=['level_0'], inplace=True)
    df_ingredient_NDB.reset_index(inplace=True)
    if 'level_0' in df_ingredient_NDB.columns:
        df_ingredient_NDB.drop(columns=['level_0'], inplace=True)

    return df_ingredient_NDB, df_ingredient_NDBi
