from keras.models import load_model, model_from_json
import pickle
import re
import numpy as np
from scipy.optimize import linprog
import pandas as pd
pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
from rootseller import recipes
from rootseller import rootprofile

class Models(object):
    def __init__(self, recipe_init):
        with open('C:/Users/mgruz/Desktop/w210/data/models/tokenizer.pickle', 'rb') as handle:
            self.tokenizer = pickle.load(handle)
        # load json and create model
        with open('C:/Users/mgruz/Desktop/w210/data/models/model_simple_nn.json', 'rb') as nn_model:
            nn_model_file = pickle.load(nn_model)
            self.nn_model = model_from_json(nn_model_file)
            self.nn_model.load_weights("C:/Users/mgruz/Desktop/w210/data/models/model_simple_nn_WEIGHTS.h5")

        self.recipe_init = recipe_init

    def transform_data_for_tokenizer(self, recipe_item):
        original = recipe_item.lower()
        original = re.sub(r'\s*(\d+|[./+*-])', '', original)
        original_split = original.split(" ")

        units_of_food_recipe_list = []
        for key in self.recipe_init.food_unit_standard_dictionary:
            for sub_key in self.recipe_init.food_unit_standard_dictionary[key]:
                units_of_food_recipe_list.append(sub_key)

        keep_list = []
        for i in original_split:
            if i not in self.recipe_init.food_size and i not in units_of_food_recipe_list:
                keep_list.append(i)

        original_split = list(filter(None, keep_list))
        new = " ".join(original_split)
        return new

user_init = profile.UserProfile('mikegruzynski')
recipe_init = recipes.Recipes(user_init)
models_init = Models(recipe_init)

ingredient = '1 large egg'
ingredient_filtered = models_init.transform_data_for_tokenizer(ingredient)

print(ingredient)

tokens = models_init.tokenizer.texts_to_matrix([ingredient_filtered])
prediction = models_init.nn_model.predict(np.array(tokens))
