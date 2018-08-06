import pandas as pd
# pd.set_option('display.height', 1000)
# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 500)
# pd.set_option('display.width', 1000)
from app.user_profile_support.rootseller import micronutrients
from app.user_profile_support.rootseller import macronutrients
from app.user_profile_support.calculate_macro_nutrients import get_macro_label_list
from app.user_profile_support.get_user_nutrients import get_micro_label_list

class UserProfile(object):
    def __init__(self, user_profile_data):
        self.userid = user_profile_data.username
        self.userprofile_df = user_profile_data
        
        init_macro = macronutrients.Macronutrients(self.userprofile_df)
        init_micro = micronutrients.MicroNutrients(self.userprofile_df)

        # Get user Specified Macro List From Prefernece Survey
        self.macro_label_list = get_macro_label_list(user_profile_data.user_macro_choices.values[0])
        print(self.macro_label_list )
        self.macro_list = init_macro.convert_labels_to_df_columns(self.macro_label_list)

        # TODO:
        print("\n***TODO ROOTPROFILE EDIT **** ")
        # Get user Specified Micro List From Prefernece Survey
        self.micro_label_list = ['iron', 'magnesium', 'manganese', 'thiamin', 'Vitamin D']
        # self.micro_label_list = get_micro_label_list(user_profile_data.user_micro_choices.values[0])
        print(self.micro_label_list)
        self.micro_list = init_micro.convert_labels_to_df_columns(self.micro_label_list)

        self.profile_macro_df = init_macro.macro_daily_macro_estimation(user_profile_data)
        self.profile_micro_df = init_micro.micro_daily_macro_estimation(user_profile_data)

        self.profile_macro_filtered_df = self.profile_macro_df[self.macro_label_list]
        self.profile_micro_filtered_df = self.profile_micro_df[self.micro_list]
