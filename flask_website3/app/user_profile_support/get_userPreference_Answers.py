import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from app.user_profile_support.calculate_macro_nutrients import get_macro_label_list
from app.user_profile_support.get_user_nutrients import get_micro_label_list
from flask import session

def get_userPreferences(user):
    # Returns the user preferences from the google Form
    # Get User Prefernece Results from Google Drive for users
    # if None exist in data, return
    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']
    print("Getting Survey Responses")
    cred_path = 'app/static/csv_files/'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_path + 'w210-e41e21aed377.json', scope)
    print("Success!")
    # Get Google Sheet of Reponses
    gc = gspread.authorize(credentials)
    wks = gc.open("User preference survey (Responses)").sheet1
    userPref_df = pd.DataFrame(wks.get_all_records(), dtype=str)
    print("userPref_df complete!")
    print(userPref_df.columns)
    # Rename columns for easier use
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
      'Timestamp':'timestamp',
      'How Many Recipes Would You Like to Plan per Week?':'meals_per_week'}

    userPref_df.rename(columns=rename_dict, inplace=True)
    print(userPref_df.columns)
    # Look for user if exists in user preferneces
    if any(userPref_df.username == user):
        print(user)
        user_prefs = userPref_df[userPref_df.username == user]
        # Choose Most Recent Answers
        if len(user_prefs > 1):
            user_prefs = user_prefs[user_prefs.timestamp == user_prefs.timestamp.max()]

            # Get list of nutritional labels user is interested in
            filter_list = get_macro_label_list(user_prefs.user_macro_choices.values[0])
            filter_list = get_micro_label_list(user_prefs.user_macro_choices.values[0])
            user_prefs['filter_list'] = [filter_list]
            # user_prefs['plan_exists'] = False

        print("Returning user preferenecs")
        # return userPref_df
        return user_prefs
    else:
        print("returning False")
        # Send to the user new user_profile page to fill out preferneces
        return False


def create_ignore_list_from_session_df(session):
    if 'ignore_list' in session.keys():
        existing_ignores = pd.read_json(session['ignore_list'])
        ignore_list = []
        for ignore in existing_ignores.recipe_ignore.values:
            ignore_list = ignore_list + ignore.split(', ')
    return ignore_list


def process_ignore_form(session, ignore_form):
    if 'ignore_list' in session.keys():
        existing_ignore_list = create_ignore_list_from_session_df(session)
    ignore_list1 = ignore_form.ignore_list.data.split('RECIPE_ ')
    ignore_list = []
    for recipe_id in ignore_list1:
        ignore_list = ignore_list + recipe_id.split(', ')
    ignore_list = existing_ignore_list + ignore_list
    session['ignore_list'] = pd.DataFrame({'recipe_ignore':ignore_list}).to_json()


def get_user_ignore_responses(user_profile_data, user):
    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']

    cred_path = 'app/static/csv_files/'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_path + 'w210-e41e21aed377.json', scope)

    # Get Google Sheet of Reponses
    gc = gspread.authorize(credentials)
    wks2 = gc.open("Recipe Removal (Responses)").sheet1
    all_user_ignore_df = pd.DataFrame(wks2.get_all_records(), dtype=str)

    rename_dict = {'Please re-enter your Root Cellar username': 'username',
    'Please list recipe ID\'s you would like to see removed (separate by commas).':'ignore_list'}
    all_user_ignore_df.rename(columns=rename_dict, inplace=True)

    ignore_list = []
    # Look for user if exists in user preferneces
    if any(all_user_ignore_df.username == user):
        user_ignore_df = all_user_ignore_df[all_user_ignore_df.username == user]
        for ignore in user_ignore_df.ignore_list.values:
            ignore_list = ignore_list + ignore.split(', ')

    session['ignore_list'] = pd.DataFrame({'recipe_ignore':ignore_list}).to_json()
    # user_profile_data.ignore_list = ignore_list
    return ignore_list
