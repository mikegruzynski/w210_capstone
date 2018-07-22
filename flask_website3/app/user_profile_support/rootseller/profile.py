# import pandas as pd
# # pd.set_option('display.height', 1000)
# # pd.set_option('display.max_rows', 500)
# # pd.set_option('display.max_columns', 500)
# # pd.set_option('display.width', 1000)
# from app.user_profile_support.rootseller import micronutrients
# from app.user_profile_support.rootseller import macronutrients
#
#
#
# class UserProfile(object):
#
#     def __init__(self, userid):
#         try:
#             userprofile_df = pd.read_csv('C:/Users/mgruz/Desktop/w210/data/user/userprofile.csv')
#         except:
#             userprofile_df = pd.read_csv('C:/Users/pa351d/Desktop/w210/data/user/userprofile.csv')
#
#
#         self.userid = userid
#         self.userprofile_df = userprofile_df[userprofile_df['userid'] == self.userid]
#
#         init_macro = macronutrients.Macronutrients(self.userprofile_df)
#         init_micro = micronutrients.MicroNutrients(self.userprofile_df)
#
#         self.macro_label_list = eval(self.userprofile_df['macro_nutrients'].get_values()[0])
#         self.macro_list = init_macro.convert_labels_to_df_columns(self.macro_label_list)
# 
#         self.micro_label_list = eval(self.userprofile_df['micro_nutrients'].get_values()[0])
#         self.micro_list = init_micro.convert_labels_to_df_columns(self.micro_label_list)
#
#         self.profile_macro_df = init_macro.macro_daily_macro_estimation()
#         self.profile_micro_df = init_micro.micro_daily_macro_estimation()
#
#         self.profile_macro_filtered_df = self.profile_macro_df[self.macro_label_list]
#         self.profile_micro_filtered_df = self.profile_micro_df[self.micro_list]
