import pandas as pd
pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

class Macronutrients(object):
    def __init__(self, user_df):
        self.user_df = user_df
        self.macronutrient_column_map_dict = {
            'calories': {'map_key': 'Energy (kcal)', 'unit': 'kcal'},
            'fat': {'map_key': 'Total lipid (fat) (g)', 'unit': 'g'},
            'carbohydrate': {'map_key': 'Carbohydrate, by difference (g)', 'unit': 'g'},
            'fiber': {'map_key': 'Fiber, total dietary (g)', 'unit': 'g'},
            'cholesterol': {'map_key': 'Cholesterol (mg)', 'unit': 'mg'},
            'saturated_fat': {'map_key': 'Fatty acids, total saturated (g)', 'unit': 'g'},
            'unsaturated_fat': {'map_key': ["Fatty acids, total monounsaturated (g)", "Fatty acids, total polyunsaturated (g)", "Fatty acids, total trans (g)"], 'unit': 'g'},
            'sugar': {'map_key': 'Sugars, total (g)', 'unit': 'g'},
            'protein': {'map_key': 'Protein (g)', 'unit': 'g'}
        }


    def macro_daily_macro_estimation(self):
        height_split = self.user_df['height'].get_values()[0]
        height_split = height_split.split("'")
        height = float(height_split[0]) * 12.0 + float(height_split[-1].strip('"'))
        del height_split

        weight = float(self.user_df['weight'].get_values()[0])
        age = float(self.user_df['age'].get_values()[0])

        if self.user_df['activity_level'].get_values()[0] == 'none':
            calorie_factor = 1.2
            protein_factor = 0.4
        elif self.user_df['activity_level'].get_values()[0] == 'low':
            calorie_factor = 1.375
            protein_factor = 0.75
        elif self.user_df['activity_level'].get_values()[0] == 'moderate':
            calorie_factor = 1.55
            protein_factor = 0.75
        elif self.user_df['activity_level'].get_values()[0] == 'heavy':
            calorie_factor = 1.9
            protein_factor = 1.0

        profile_dict = {}

        if self.user_df['gender'].get_values()[0] == 'male':
            # The Original Harris-Benedict Equation
            calories = 66.473 + 13.7516 * (weight / 2.2) + 5.0033 * (height * 2.54) - 6.755 * age
            calories = round(calories * calorie_factor, 1)
        elif self.user_df['gender'].get_values()[0] == 'female':
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

        macro_df = pd.DataFrame({'calories': [calories],
                                 'protein': [protein],
                                 'fat': [fat],
                                 'carbohydrate': [carbohydrates],
                                 'fiber': [fiber],
                                 'cholesterol': [cholesterol],
                                 'saturated_fat': [saturated_fat],
                                 'unsaturated_fat': [unsaturated_fat],
                                 'sugar': [sugar]
                                 })

        return macro_df


    def convert_labels_to_df_columns(self, micro_nutritents_interest_list):
        new_macro_list = []
        for macro in micro_nutritents_interest_list:
            if isinstance(self.macronutrient_column_map_dict[macro]['map_key'], list):
                for item in self.macronutrient_column_map_dict[macro]['map_key']:
                    new_macro_list.append(item)
            else:
                new_macro_list.append(self.macronutrient_column_map_dict[macro]['map_key'])
        return new_macro_list
