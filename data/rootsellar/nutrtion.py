import pandas as pd
pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
from rootseller import profile
from rootseller import micronutrients
from rootseller import macronutrients


class Nutrition(object):
    def __init__(self):
        try:
            self.nutritional_database = pd.read_csv('C:/Users/mgruz/Desktop/w210/data/nutrient/compiled/nutrition_master_df.csv').fillna(0.0)
        except:
            self.nutritional_database = pd.read_csv('C:/Users/pa351d/Desktop/w210/data/nutrient/compiled/nutrition_master_df.csv').fillna(0.0)


    def NDB_NO_lookup(self, tag, **kwargs):

        if "filter_list" in kwargs.keys():
            return self.nutritional_database[self.nutritional_database['NDB_NO'] == "\"{}\"".format(tag.strip('"'))][kwargs["filter_list"]]
        else:
            return self.nutritional_database[self.nutritional_database['NDB_NO'] ==  "\"{}\"".format(tag.strip('"'))]
