import pandas as pd

class Nutrition(object):
    def __init__(self):
        path = 'app/static/csv_files/'
        self.nutritional_database = pd.read_csv(path+'nutrition_master_df.csv').fillna(0.0)
        self.nutritional_normalized_database = pd.read_csv(path+'nutrition_master_normalized_df.csv').fillna(0.0)

    def NDB_NO_lookup(self, tag, **kwargs):
        if "filter_list" in kwargs.keys():
            return self.nutritional_database[self.nutritional_database['NDB_NO'] == "\"{}\"".format(tag.strip('"'))][kwargs["filter_list"]]
        else:
            return self.nutritional_database[self.nutritional_database['NDB_NO'] ==  "\"{}\"".format(tag.strip('"'))]

    def NDB_NO_lookup_normalized(self, tag, **kwargs):

        if "filter_list" in kwargs.keys():
            return self.nutritional_normalized_database[self.nutritional_normalized_database['NDB_NO'] == "\"{}\"".format(tag.strip('"'))][kwargs["filter_list"]]
        else:
            return self.nutritional_normalized_database[self.nutritional_normalized_database['NDB_NO'] ==  "\"{}\"".format(tag.strip('"'))]
