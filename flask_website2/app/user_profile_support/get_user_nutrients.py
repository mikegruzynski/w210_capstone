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

# List User Specified Micros by name
def get_micro_label_list(user_micro_choices):
    micro_pref_list = user_micro_choices.split(', ')
    micro_list = []
    all_list = ['Vitamin A', 'vitamin B12', 'retinol', 'vitamin B6', 'folate',
    'manganese', 'sodium', 'zinc', 'vitamin C', 'Vitamin D', 'vitamin E',
    'Vitamin K', 'calcium', 'iron', 'betaine', 'choline', 'pantothenic',
    'riboflavin', 'phosphorus', 'magnesium', 'potassium', 'copper',
    'selenium', 'fluoride', 'thiamin', 'niacin', 'folic acid']

    for micro in micro_pref_list:
        if (micro == 'All') |  (micro == ''):
            micro_list = all_list
            continue
        elif micro == 'None':
            micro_list = None
            continue
        elif micro == 'Vitamin A':
            micro_list = micro_list + ['Vitamin A']
        elif micro == 'Vitamin B12':
            micro_list = micro_list + ['vitamin B12']
        elif micro == 'Retinol':
            micro_list = micro_list + ['retinol']
        elif micro == 'Vitamin B6':
            micro_list = micro_list + ['vitamin B6']
        elif micro == 'Folate (Vitamin B9)':
            micro_list = micro_list + ['folate']
        elif micro == 'Manganese':
            micro_list = micro_list + ['manganese']
        elif micro == 'Sodium':
            micro_list = micro_list + ['sodium']
        elif micro == 'Zinc':
            micro_list = micro_list + ['zinc']
        elif micro == 'Vitamin C':
            micro_list = micro_list + ['vitamin C']
        elif micro == 'Vitamin D':
            micro_list = micro_list + ['Vitamin D']
        elif micro == 'Vitamin E':
            micro_list = micro_list + ['vitamin E']
        elif micro == 'Vitamin K':
            micro_list = micro_list + ['Vitamin K']
        elif micro == 'Calcium':
            micro_list = micro_list + ['calcium']
        elif micro == 'Iron':
            micro_list = micro_list + ['iron']
        elif micro == 'Betaine':
            micro_list = micro_list + ['betaine']
        elif micro == 'Choline':
            micro_list = micro_list + ['choline']
        elif micro == 'Pantothenic':
            micro_list = micro_list + ['pantothenic']
        elif micro == 'Riboflavin':
            micro_list = micro_list + ['riboflavin']
        elif micro == 'Phosphorus':
            micro_list = micro_list + ['phosphorus']
        elif micro == 'Magnesium':
            micro_list = micro_list + ['magnesium']
        elif micro == 'Potassium':
            micro_list = micro_list + ['potassium']
        elif micro == 'Copper':
            micro_list = micro_list + ['copper']
        elif micro == 'Selenium':
            micro_list = micro_list + ['selenium']
        elif micro == 'Fluoride':
            micro_list = micro_list + ['fluoride']
        elif micro == 'Thiamin':
            micro_list = micro_list + ['thiamin']
        elif micro == 'Niacin':
            micro_list = micro_list + ['niacin']
        elif micro == 'Folic acid':
            micro_list = micro_list + ['folic acid']

    return(micro_list)
