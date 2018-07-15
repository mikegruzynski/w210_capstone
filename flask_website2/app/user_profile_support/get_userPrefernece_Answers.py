import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def get_userPreferences(user):
    # Returns the user preferences from teh googo
    # Get User Prefernece Results from Google Drive for users
    # if None exist in data, return
    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']

    cred_path = 'app/static/csv_files/'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_path + 'w210-e41e21aed377.json', scope)

    gc = gspread.authorize(credentials)

    wks = gc.open("User preference survey (Responses)").sheet1
    userPref_df = pd.DataFrame(wks.get_all_records(), dtype=str)

    # Rename columns
    rename_dict = {'How frequently do you exercise?': 'activity_level',
      'How much time are you willing to spend on a meal?': 'meal_prep_time',
      'If you are interested in tracking macros, please indicate which of the following are important to you': 'user_macro_choices',
      'If you are interested in tracking micros, please indicate which of the following are important to you': 'user_micro_choices',
      'Please re-enter your Root Cellar username': 'username',
      'Timestamp': u'7/9/2018 19:43:02',
      'What are you looking for in a nutrition app? (Multiple choice)': '',
      'What foods are you allergic to? (Please separate each item with a comma)': 'allergies',
      'What is your age?': 'age',
      'What is your current / aspired diet type? (Pick the one that most applies to you)': 'diet',
      'What is your gender?': 'gender',
      'What is your height (in inches)?': 'height_in',
      'What is your weight (in lbs)?': 'weight_lb',
      'Which of the following apply to you? (Multiple choice)': 'dietary_restrictions'}

    userPref_df.rename(columns=rename_dict, inplace=True)

    # Look for user if exists in user preferneces
    if any(userPref_df.username == 'user_mc'):
        user_prefs = userPref_df[userPref_df.username == 'user_mc']
        user_prefs = user_prefs.to_dict()
        return(user_prefs)
    else:
        # Send to the user new user_profile page to fill out preferneces
        return(False)
