import pandas as pd
from app.user_profile_support.calculate_macro_nutrients import *

def get_micro_nutrients(user_pref_dict, user_micro_choices=False):
    # Uses User Prefernces Dictionary to use Look up Table to return Micro Nutrients
    micros_df= pd.read_csv('app/static/csv_files/micros_csv.csv')

    ud = micros_df.loc[(micros_df.age_low <= user_pref_dict.get('age')) &
    (micros_df.age_high >= user_pref_dict.get('age')) &
    (micros_df.gender == user_pref_dict.get('gender')) &
     (micros_df.is_pregnant == user_pref_dict.get('is_pregnant')) &
     (micros_df.is_breastfeeding == user_pref_dict.get('is_breastfeeding'))]

    # Only Report the ones User is interested in
    if user_micro_choices is not False:
        ud = ud[user_micro_choices]

    # Check only one row was returned
    ud.reset_index(drop=True, inplace=True)
    if len(ud) == 0:
        print("No Micros Data Found Matching ")
        ud={}
    elif len(ud) == 1:
        user_micros_dict = ud.to_dict()
    else:
        print("Choosing only first row of data found in dictionary")
        user_micros_dict = ud[0].to_dict()

    return user_micros_dict

def get_macro_nutrients(user_pref_dict):

    macros_dict = calculate_macros(user_pref_dict)
    # macros_dict = dict(calories=2000, carbs=467.3,
    # protein=142.5, fat=67.8, cholesterol=300.0,
    # sat_fat=33.9, unsat_fat=101.6, sugar=33.9)

    return macros_dict
