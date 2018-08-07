import pandas as pd
import numpy as np
from app.user_profile_support.get_userPreference_Answers import *
from app.user_profile_support.ingredientSubsitutions import get_recipe_list

def return_user_meal_plan(session, user_profile_data, user):
    # Get Recipe Reccomendations for the user
    if 'user_meal_plan' not in session.keys():
        best_recipe_combo, weekly_diet_amount, user_profile_data, df_ingredient_NDB = get_recipe_list(session, user)

    user_meal_plan = pd.read_json(session['user_meal_plan'])
    best_recipe_combo = user_meal_plan.recipe_id

    # Sanity Check the ignore list before returning Results. If a recipe is in ignore list run again
    ignore_list = get_user_ignore_responses(session, user)
    # if 'ignore_list' in session.keys():
    #     old_ignore_list = create_ignore_list_from_session_df(session)
    #     ignore_list = ignore_list + old_ignore_list
    # session['ignore_list'] = pd.DataFrame({'recipe_ignore':ignore_list}).to_json()

    while any(np.intersect1d(ignore_list, user_meal_plan.recipe_id)):
        best_recipe_combo, weekly_diet_amount, user_profile_data, df_ingredient_NDB = get_recipe_list(session, user)
        user_meal_plan = pd.read_json(session['user_meal_plan'])

    return(user_meal_plan)
