import pandas as pd
# pd.set_option('display.height', 1000)
# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 500)
# pd.set_option('display.width', 1000)
from app.user_profile_support.rootseller import micronutrients
from app.user_profile_support.rootseller import macronutrients

class UserProfile(object):
    def __init__(self, user_profile_data):
        # TODO: get info from real user profile not fake Mike's
        # userprofile_df = pd.read_csv('app/static/csv_files/temp/userprofile.csv')

        self.userid = user_profile_data.username
        self.userprofile_df = user_profile_data

        init_macro = macronutrients.Macronutrients(self.userprofile_df)
        init_micro = micronutrients.MicroNutrients(self.userprofile_df)

        # self.macro_label_list = eval(self.userprofile_df['macro_nutrients'].get_values()[0])
        # TODO: get from User Profile instead. Fix the map to match the user survey
        # this is the all list
        self.macro_label_list = ['calories', 'fat', 'carbohydrate', 'fiber',
        'cholesterol', 'saturated_fat', 'unsaturated_fat', 'sugar', 'protein']
        self.macro_list = init_macro.convert_labels_to_df_columns(self.macro_label_list)

        # self.micro_label_list = eval(self.userprofile_df['micro_nutrients'].get_values()[0])
        # this is the all list
        # self.micro_label_list = ['calcium', 'iron', 'magnesium', 'phosphorus',
        # 'potassium', 'sodium', 'zinc', 'copper', 'manganese', 'selenium', 'fluoride',
        # 'vitamin C', 'thiamin', 'riboflavin', 'niacin', 'pantothenic',
        # 'vitamin B6', 'folate', 'folic acid', 'choline', 'betaine',
        # 'vitamin B12', 'Vitamin A', 'retinol', 'vitamin E', 'Vitamin D', 'Vitamin K']
        self.micro_label_list = ['iron', 'magnesium', 'manganese', 'thiamin', 'Vitamin D']
        self.micro_list = init_micro.convert_labels_to_df_columns(self.micro_label_list)

        self.profile_macro_df = init_macro.macro_daily_macro_estimation(user_profile_data)
        self.profile_micro_df = init_micro.micro_daily_macro_estimation(user_profile_data)

        self.profile_macro_filtered_df = self.profile_macro_df[self.macro_label_list]
        self.profile_micro_filtered_df = self.profile_micro_df[self.micro_list]
