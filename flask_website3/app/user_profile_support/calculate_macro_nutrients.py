import pandas as pd

def calculate_macros(user_profile_data):
    # user_profile_dict - contains the users information
    # return macors_dictionary for user
    height = int(user_profile_data.height_in.values[0])
    weight = int(user_profile_data.weight_lb.values[0])
    activity_level = user_profile_data.activity_level.values[0]
    age = int(user_profile_data.age.values[0])

    if activity_level == 'Little to no exercise':
        calorie_factor = 1.2
        protein_factor = 0.4
    elif activity_level == 'Exercise 1-3 times per week':
        calorie_factor = 1.375
        protein_factor = 0.75
    elif activity_level == 'Exercise 3-5 times per week':
        calorie_factor = 1.55
        protein_factor = 0.75
    elif (activity_level == 'Exercise 6+ times per week') or (activity_level == 'Exercise 6+ times per week?'):
        calorie_factor = 1.9
        protein_factor = 1.0

    profile_dict = {}

    if user_profile_data.gender.values[0] == 'Male':
        # The Original Harris-Benedict Equation
        calories = 66.473 + 13.7516 * (weight / 2.2) + 5.0033 * (height * 2.54) - 6.755 * age
        calories = round(calories * calorie_factor, 1)
    elif user_profile_data.gender.values[0] == 'Female':
        calories = 655.0955 + 9.5634 * (int(weight) / 2.2) + 1.8496 * (height * 2.54) - 4.6756 * age
        calories = round(calories * calorie_factor, 1)
    elif user_profile_data.gender.values[0] == 'Prefer Not to Say':
        # Using Male Calculation if geder is unknown
        calories = 66.473 + 13.7516 * (weight / 2.2) + 5.0033 * (height * 2.54) - 6.755 * age
        calories = round(calories * calorie_factor, 1)

    # Proteins (g)
    protein = round(weight * protein_factor, 1)

    # Fats (g)
    fat = round((calories * 0.2) / 9.0, 1)

    # Carbohydrates (g)
    carbohydrates = round((calories - ((protein * 4.0) + (fat * 9.0))) / 4.0, 1)

    # Fiber (g)
    fiber = round((calories / 1000.0) * 14.0, 1)

    # Cholesterol (mg)
    cholesterol = 300.0

    # Saturated Fat (g)
    saturated_fat = round((calories * 0.1) / 9.0, 1)

    # Unsaturated Fat (g)
    unsaturated_fat = round((calories * 0.3) / 9.0, 1)

    # Sugar (g)
    sugar = round((calories * 0.1) / 9.0, 1)

    macros_dict = {'calories': [calories],
                             'protein': [protein],
                             'fat': [fat],
                             'carbohydrate': [carbohydrates],
                             'fiber': [fiber],
                             'cholesterol': [cholesterol],
                             'saturated_fat': [saturated_fat],
                             'unsaturated_fat': [unsaturated_fat],
                             'sugar': [sugar]
                             }

    return macros_dict


# Creates list of macro ingredients that which the user specifies.
def get_macro_label_list(user_macro_choices):
    macro_pref_list = user_macro_choices.split(', ')
    macro_list = []
    all_list = ['calories', 'fat', 'carbohydrate', 'fiber', 'cholesterol',
                'saturated_fat', 'unsaturated_fat', 'sugar', 'protein']
    for macro in macro_pref_list:
        if macro == 'All':
            macro_list = all_list
            continue
        elif macro == '':
            # If undefined choices choose all
            macro_list = all_list
            continue
        elif macro == 'None':
            macro_list = None
            continue
        elif macro == 'Protiens':
            macro_list = macro_list + ['protein']
        elif macro == 'Fats':
            macro_list = macro_list + ['unsaturated_fat']
            macro_list = macro_list + ['saturated_fat']
            macro_list = macro_list + ['fat']
        elif macro == 'Carbohydrates':
            macro_list = macro_list + ['carbohydrate']
        elif macro == 'Cholesterol':
            macro_list = macro_list + ['cholesterol']
        elif macro == 'Sugars':
            macro_list = macro_list + ['sugar']
        elif macro == 'Fiber':
            macro_list = macro_list + ['fiber']
        elif macro == 'Calories':
            macro_list = macro_list + ['calories']
    return(macro_list)
