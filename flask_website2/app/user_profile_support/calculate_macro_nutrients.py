import pandas as pd

def calculate_macros(user_profile_dict):
    # user_profile_dict - contains the users information
    # return macors_dictionasry for user

    height = user_profile_dict.get('height_in')
    weight = user_profile_dict.get('weight_lb')
    activity_level = user_profile_dict.get('activity_level')
    age = user_profile_dict.get('age')

    if activity_level == 'none':
        calorie_factor = 1.2
        protein_factor = 0.4
    elif activity_level == 'low':
        calorie_factor = 1.375
        protein_factor = 0.75
    elif activity_level == 'moderate':
        calorie_factor = 1.55
        protein_factor = 0.75
    elif activity_level == 'heavy':
        calorie_factor = 1.9
        protein_factor = 1.0

    profile_dict = {}

    if user_profile_dict.get('gender') == 'Male':
        # The Original Harris-Benedict Equation
        calories = 66.473 + 13.7516 * (weight / 2.2) + 5.0033 * (height * 2.54) - 6.755 * age
        calories = round(calories * calorie_factor, 1)
    elif user_profile_dict.get('gender') == 'Female':
        calories = 655.0955 + 9.5634 * (weight / 2.2) + 1.8496 * (height * 2.54) - 4.6756 * age
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
