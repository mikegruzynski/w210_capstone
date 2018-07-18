import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# TODO: Fix pick up of user input of

def get_userPreferences(user):
    # Returns the user preferences from the google Form
    # Get User Prefernece Results from Google Drive for users
    # if None exist in data, return
    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']

    cred_path = 'app/static/csv_files/'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_path + 'w210-e41e21aed377.json', scope)

    gc = gspread.authorize(credentials)

    wks = gc.open("User preference survey (Responses)").sheet1
    userPref_df = pd.DataFrame(wks.get_all_records(), dtype=str)

    #  All macros
    all_macros = ['Energy (kcal)', 'Total lipid (fat) (g)',
    'Carbohydrate, by difference (g)', 'Fiber, total dietary (g)',
    'Cholesterol (mg)', 'Fatty acids, total saturated (g)',
    'Fatty acids, total monounsaturated (g)',
    'Fatty acids, total polyunsaturated (g)', 'Fatty acids, total trans (g)',
    'Sugars, total (g)', 'Protein (g)']
    # All micros
    all_mircros =  ['Iron, Fe (mg)', 'Magnesium, Mg (mg)', 'Manganese, Mn (mg)',
    'Thiamin (mg)', 'Vitamin D (D2 + D3) (microg)']
    # ['Alanine (g)', 'Alcohol, ethyl (g)',	'Arginine (g)', 'Ash (g)'
    # 	'Aspartic acid (g)',	'Beta-sitosterol (mg)',	'Betaine (mg)',
    #     'Caffeine (mg)',	'Calcium, Ca (mg)',	'Campesterol (mg)',
    #     'Carbohydrate, by difference (g)', 	'Carotene, alpha (microg)',
    #     'Carotene, beta (microg)', 'Cholesterol (mg)',	'Choline, total (mg)',
    #     'Copper, Cu (mg)', 	'Cryptoxanthin, beta (microg)', 'Cystine (g)',
    #     'Dihydrophylloquinone (microg)', 'Fluoride, F (microg)',
    #     'Folate, DFE (microg)',	'Folate, food (microg)', 'Folate, total (microg)',
    #     'Folic acid (microg)', 	'Fructose (g)', 'Galactose (g)',
    #     'Glucose (dextrose) (g)', 'Glutamic acid (g)', 	'Glycine (g)',
    #     'Histidine (g)', 'Hydroxyproline (g)', 	'Iron, Fe (mg)'	, 'Lactose (g)',
    #     'Leucine (g)', 	'Lutein + zeaxanthin (microg)', 'Lycopene (microg)', 'Lysine (g)',
    #     'Magnesium, Mg (mg)', 'Maltose (g)', 'Manganese, Mn (mg)', 	'Methionine (g)',
    #     'Niacin (mg)',	'Pantothenic acid (mg)',	'Phenylalanine (g)',
    #     'Phosphorus, P (mg)', 'Phytosterols (mg)', 'Potassium, K (mg)',
    #     'Proline (g)', 'Retinol (microg)', 	'Riboflavin (mg)', 	'Selenium, Se (microg)',
    #     'Sodium, Na (mg)', 'Starch (g)', 'Stigmasterol (mg)',  'Sucrose (g)',
    #     'Sugars, total (g)', 'Theobromine (mg)', 'Thiamin (mg)', 'Threonine (g)',
    #     'Tocopherol, beta (mg)', 'Tocopherol, delta (mg),'	'Tocopherol, gamma (mg)',
    #     'Tocotrienol, alpha (mg)', 'Tocotrienol, beta (mg)', 'Tocotrienol, delta (mg)',
    #     'Tocotrienol', 'gamma (mg)', 'Total lipid (fat) (g)', 'Tryptophan (g)',
    #     'Tyrosine (g)', 'Valine (g)', 'Vitamin A, IU (IU)', 'Vitamin A, RAE (microg)',
    #     'Vitamin B-12 (microg)', 'Vitamin B-12, added (microg)', 	'Vitamin B-6 (mg)',
    #     'Vitamin C, total ascorbic acid (mg)', 'Vitamin D (D2 + D3) (microg)',	'Vitamin D (IU)',
    #     'Vitamin D2 (ergocalciferol) (microg)', 'Vitamin D3 (cholecalciferol) (microg)',
    #     'Vitamin E (alpha-tocopherol) (mg)', 'Vitamin E, added (mg)',
    #     'Vitamin K (phylloquinone) (microg)',
    #      'Zinc, Zn (mg)', 'Serine (g)']


    # Rename columns
    rename_dict = {'How frequently do you exercise?': 'activity_level',
      'How much time are you willing to spend on a meal?': 'meal_prep_time',
      'If you are interested in tracking macros, please indicate which of the following are important to you': 'user_macro_choices',
      'If you are interested in tracking micros, please indicate which of the following are important to you': 'user_micro_choices',
      'Please re-enter your Root Cellar username': 'username',
      'Timestamp': u'7/9/2018 19:43:02',
      'What are you looking for in a nutrition app? (Multiple choice)': '',
      'What foods are you allergic to? (Please separate each item with a comma)': 'allergies',
      'Age': 'age',
      'First Name': 'firstname',
      'Last Name': 'lastname',
      'Are you Pregnant or Breastfeeding ': 'is_pregnant_breastfeeding',
      'What is your current / aspired diet type? (Pick the one that most applies to you)': 'diet',
      'What is your gender?': 'gender',
      'What is your height (in inches)?': 'height_in',
      'What is your weight (in lbs)?': 'weight_lb',
      'What foods are you allergic to or dislike? (Please separate each item with a comma)':'food_allergies',
      'Which of the following apply to you? (Multiple choice)': 'dietary_restrictions',
      'Timestamp':'timestamp'}

    userPref_df.rename(columns=rename_dict, inplace=True)

    # Look for user if exists in user preferneces
    if any(userPref_df.username == user):
        user_prefs = userPref_df[userPref_df.username == user]
        # Choose Most Recent Answers
        if len(user_prefs > 1):
            user_prefs = user_prefs[user_prefs.timestamp == user_prefs.timestamp.max()]

            # Add List of micro and macros the user is interested in
            if user_prefs.user_macro_choices.values[0] == 'All':
                filter_list = all_macros
            else:
                # TODO: Add Cholesterol & Sugar to survey
                macro_list = userPerf_df.user_macro_choices.values
                filter_list = []
                if 'Protiens' in macro_list:
                    filter_list = filter_list + 'Protein (g)'
                if 'Fats' in macro_list:
                    fats_list = ['Total lipid (fat) (g)',
                    'Fatty acids, total saturated (g)']
                    # 'Fatty acids, total monounsaturated (g)',
                    # 'Fatty acids, total trans (g)',
                    # 'Fatty acids, total polyunsaturated (g)']
                    filter_list = filter_list + fats_list
                if 'Carbohydrates' in macro_list:
                    filter_list = filter_list + 'Carbohydrate, by difference (g)'
                if 'Fiber' in macro_list:
                    filter_list = filter_list + 'Fiber, total dietary (g)'
                if 'Calories' in macro_list:
                    filter_list = filter_list + 'Energy (kcal)'
                if 'Cholesterol' in macro_list:
                    filter_list = filter_list + 'Cholesterol (mg)'
                if 'Sugar' in macro_list:
                    filter_list = filter_list + 'Sugars, total (g)'


            # Add Micros to Filter List
            if user_prefs.user_micro_choices.values[0] == 'All':
                filter_list = filter_list + all_mircros
            else:
                # TODO:
                filter_list = filter_list + userPerf_df.user_micro_choices

            # user_prefs['filter_list'] = [filter_list]
        return user_prefs
    else:
        # Send to the user new user_profile page to fill out preferneces
        return(False)
