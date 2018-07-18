# Code to support Ingredient subsitions
# Mostly from master_run in rootsellar folder
recipe_itr = 0
from app.user_profile_support.rootseller import rootprofile
from app.user_profile_support.rootseller import recipes, research
from app.user_profile_support.rootseller.recipes import Recipes
import pandas as pd

def run_master_ingredient_sub(user_profile_data, list_keys):
    # profile_init = rootprofile.UserProfile('mikegruzynski')
    profile_init = rootprofile.UserProfile(user_profile_data)
    recipe_init = recipes.Recipes(profile_init)
    research_init = research.Research(profile_init)

    recipe_itr = 0
    df_list = []
    df_summed_list = []
    recipe_id_list = []
    name_list = []
    for recipe in list_keys:
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

    return df, df_list


# Single food Subsitution
# def single_food_subsitution():
