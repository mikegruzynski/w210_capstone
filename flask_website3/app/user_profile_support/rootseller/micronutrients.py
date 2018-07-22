import pandas as pd

class MicroNutrients(object):
    def __init__(self, user_df):
        self.micronutrient_column_map_dict = {
            'calcium': {'map_key': {'map_key': 'Calcium, Ca (mg)', 'unit': 'mg'}, 'unit': 'mg'},
            'iron': {'map_key': 'Iron, Fe (mg)', 'unit': 'mg'},
            'magnesium': {'map_key': 'Magnesium, Mg (mg)', 'unit': 'mg'},
            'phosphorus': {'map_key': 'Phosphorus, P (mg)', 'unit': 'mg'},
            'potassium': {'map_key': 'Potassium, K (mg)', 'unit': 'mg'},
            'sodium': {'map_key': 'Sodium, Na (mg)', 'unit': 'mg'},
            'zinc': {'map_key': 'Zinc, Zn (mg)', 'unit': 'mg'},
            'copper': {'map_key': 'Copper, Cu (mg)', 'unit': 'mg'},
            'manganese': {'map_key': 'Manganese, Mn (mg)', 'unit': 'mg'},
            'selenium': {'map_key': 'Fluoride, F (microg)', 'unit': 'microg'},
            'fluoride': {'map_key': 'Selenium, Se (microg)', 'unit': 'microg'},
            'vitamin C': {'map_key': 'Vitamin C, total ascorbic acid (mg)', 'unit': 'mg'},
            'thiamin': {'map_key': 'Thiamin (mg)', 'unit': 'mg'},
            'riboflavin': {'map_key': 'Riboflavin (mg)', 'unit': 'mg'},
            'niacin': {'map_key': 'Niacin (mg)', 'unit': 'mg'},
            'pantothenic': {'map_key': 'Pantothenic acid (mg)', 'unit': 'mg'},
            'vitamin B6': {'map_key': 'Vitamin B-6 (mg)', 'unit': 'mg'},
            'folate': {'map_key': 'Folate, total (microg)', 'unit': 'microg'},
            'folic acid': {'map_key': 'Folic acid (microg)', 'unit': 'microg'},
            'choline': {'map_key': 'Choline, total (mg)', 'unit': 'mg'},
            'betaine': {'map_key': 'Betaine (mg)', 'unit': 'mg'},
            'vitamin B12': {'map_key': 'Vitamin B-12 (microg)', 'unit': 'microg'},
            'Vitamin A': {'map_key': 'Vitamin A, RAE (microg)', 'unit': 'microg'},
            'retinol': {'map_key': 'Retinol (microg)', 'unit': 'microg'},
            'vitamin E': {'map_key': 'Vitamin E (alpha-tocopherol) (mg)', 'unit': 'mg'},
            'Vitamin D': {'map_key': 'Vitamin D (D2 + D3) (microg)', 'unit': 'microg'},
            'Vitamin K': {'map_key': 'Vitamin K (phylloquinone) (microg)', 'unit': 'microg'}
        }
        self.user_df = user_df
        self.micro_df = pd.read_csv('app/static/csv_files/recommended_micro_nutrients.csv',
                                    index_col='micro_nutrient')

    def micro_daily_macro_estimation(self, user_profile_data):

        female_pregnant_filter = ["Age_14_to_18_female_pregnant", "Age_19_to_9999_female_pregnant"]
        female_breastfeeding_filter = ["Age_14_to_18_female_breastfeeding", "Age_19_to_9999_female_breastfeeding"]
        female_filter = ["Age_0_to_0.5_female", "Age_0.5_to_1_female", "Age_1_to_3_female", "Age_4_to_8_female",
                         "Age_9_to_13_female", "Age_14_to_18_female", "Age_19_to_49_female", "Age_50_to_70_female",
                         "Age_71_to_9999_female"]
        male_filter = ["Age_0_to_0.5_male", "Age_0.5_to_1_male", "Age_1_to_3_male", "Age_4_to_8_male",
                            "Age_9_to_13_male", "Age_14_to_18_male", "Age_19_to_49_male", "Age_50_to_70_male",
                            "Age_71_to_9999_male"]
        if user_profile_data['gender'].values[0] == 'Male':
            column_list = male_filter
        elif user_profile_data['gender'].values[0] == 'Female':
            if user_profile_data.is_pregnant_breastfeeding.values[0] == 'Pregnant':
                column_list = female_pregnant_filter
            elif user_profile_data.is_pregnant_breastfeeding.values[0] == 'Breastfeeding':
                column_list = female_breastfeeding_filter
            else:
                column_list = female_filter

        age = int(user_profile_data['age'].values[0])

        min_age_list = []
        max_age_list = []
        for age_range in column_list:
            age_range = age_range.split("_")
            min_age_list.append(float(age_range[1]))
            max_age_list.append(float(age_range[3]))

        age_range_df = pd.DataFrame({'min_age': min_age_list,
                                     'max_age': max_age_list})[['min_age', 'max_age']]

        column_index = age_range_df[(age_range_df['min_age'] <= age) & (age_range_df['max_age'] >= age)].index.get_values()[0]

        micronutrient_series = self.micro_df.loc[:, column_list[column_index]]
        micronutrient_series.index.name = None
        micronutrient_df = micronutrient_series.to_frame().transpose().reset_index()
        del micronutrient_df['index']

        return micronutrient_df


    def convert_labels_to_df_columns(self, micro_nutritents_interest_list):

        new_micro_list = []
        for micro in micro_nutritents_interest_list:
            new_micro_list.append(self.micronutrient_column_map_dict[micro]['map_key'])

        return new_micro_list
