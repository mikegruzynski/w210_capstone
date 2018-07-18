import pandas as pd
from app.user_profile_support.calculate_macro_nutrients import *

def get_micro_nutrients(user_profile_data, user_micro_choices=False):
    # Uses User Prefernces Dictionary to use Look up Table to return Micro Nutrients
    micros_df = pd.read_csv('app/static/csv_files/micros_csv.csv')

    if user_profile_data.is_pregnant_breastfeeding.values[0] == 'No':
        is_pregnant = False
        is_breastfeeding = False
    elif user_profile_data.is_pregnant_breastfeeding.values[0] == 'Pregnant':
        is_pregnant = True
        is_breastfeeding = False
    elif user_profile_data.is_pregnant_breastfeeding.values[0] == 'Breastfeeding':
        is_pregnant = False
        is_breastfeeding = True

    ud = micros_df.loc[(micros_df.age_low <= int(user_profile_data.age.values[0])) &
    (micros_df.age_high >= int(user_profile_data.age.values[0])) &
    (micros_df.gender == user_profile_data.gender.values[0]) &
     (micros_df.is_pregnant == is_pregnant) &
     (micros_df.is_breastfeeding == is_breastfeeding)]

    # Only Report the ones User is interested in
    if user_micro_choices is not False:
        ud = ud[user_micro_choices]

    ud.reset_index(drop=True, inplace=True)
    if len(ud) == 0:
        print("No Micros Data Found Matching ")
        ud={}
    elif len(ud) == 1:
        user_micros_dict = ud.transpose().to_dict()[0]
    else:
        print("Choosing only first row of data found in dictionary")
        user_micros_dict = ud[0].transpose().to_dict()[0]

    return user_micros_dict

def get_macro_nutrients(user_profile_data):
    macros_dict = calculate_macros(user_profile_data)
    return macros_dict
