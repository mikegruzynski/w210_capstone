import json
import pandas as pd
import re
import Levenshtein
# pd.set_option('display.height', 1000)
# pd.set_option('display.max_rows', 5000)
# pd.set_option('display.max_columns', 5000)
# pd.set_option('display.width', 10000)
from app.user_profile_support.rootseller import nutrtion

class Recipes(object):
    def __init__(self, profile_init):
        path = 'app/static/csv_files/'
        with open(path+'recipe_clean_USE.json') as f:
            self.recipe_clean = json.load(f)

        self.ambiguous_df = pd.read_csv(path+'ambiguous_conversion_use.csv')

        self.user_df = profile_init.userprofile_df
        # print(self.user_df)
        self.micro_list = profile_init.micro_list
        self.macro_list = profile_init.macro_list
        # print("Micro List ", self.micro_list)
        # print("Macro List ", self.macro_list)
        self.filter_list = profile_init.micro_list + profile_init.macro_list
        # print("Filter List ", self.filter_list)
        self.nutrtion_init = nutrtion.Nutrition()

        self.food_unit_standard_dictionary = {
            'teaspoon': {'options': ["tsp.", "tsp", "t", "t.", "teaspoon", "teaspoons"], 'type': 'volume'},
            'tablespoon': {'options': ["tbsp.", "tbsp", "T", "T.", "tablespoon", "tablespoons", "tbs.", "tbs", "TBSP"], 'type': 'volume'},
            'cup': {'options': ["cups", "cup", "c.", "c"], 'type': 'volume'},
            'fl_oz': {'options': ["fl. oz.", "fl oz", "fluid ounce", "fluid ounces", "fl_oz"], 'type': 'volume'},
            'pint': {'options': ["pt", "pt.", "pint", "pints"], 'type': 'volume'},
            'quart': {'options': ["qt", "qt.", "qts", "qts.", "quart", "quarts"], 'type': 'volume'},
            'gallon': {'options': ["gal", "gal.", "gallon", "gallons"], 'type': 'volume'},
            'milliliter': {'options': ["ml", "ml.", "milliliter", "milliliters", "millilitre", "millilitres"], 'type': 'volume'},
            'liter': {'options': ["l", "l.", "liter", "liters", "litre", "litres"], 'type': 'volume'},
            'ounce': {'options': ["oz", "oz.", "ounce", "ounces", "ozs"], 'type': 'weight'},
            'pound': {'options': ["lb", "lb.", "pound", "pounds"], 'type': 'weight'},
            'milligram': {'options': ["mg", "mg.", "milligram", "milligrams", "milligramme", "milligrammes"], 'type': 'weight'},
            'gram': {'options': ["g", "g.", "gr", "gr.", "gram", "grams", "gramme", "grammes"], 'type': 'weight'},
            'kilogram': {'options': ["kg", "kg.", "kilogram", "kilograms", "kilogramme", "kilogrammes"], 'type': 'weight'},
            'pinch': {'options': ["pinch", "pinches"], 'type': 'volume'},
            'dash': {'options': ["dash", "dashes"], 'type': 'volume'},
            'touch': {'options': ["touch", "touches"], 'type': 'volume'},
            'handful': {'options': ["handful", "handfuls"], 'type': 'volume'},
            'bunch': {'options': ["bunch", "bunches"], 'type': 'volume'},
            'to_taste': {'options': ["to taste"], 'type': 'volume'},
            'drizzle': {'options': ["drizzle", "drizzled"], 'type': 'volume'},
            'sprinkle': {'options': ["sprinkle", "spinkled"], 'type': 'volume'},
            'garnish': {'options': ["garnish", "garnished"], 'type': 'volume'},
            'sprig': {'options': ["sprig", "sprigs"], 'type': 'unit'},
            'rib': {'options': ["ribs", "rib"], 'type': 'unit'},
            'sheet': {'options': ["sheets", "sheet"], 'type': 'unit'},
            'bag': {'options': ["bags", "bag"], 'type': 'unit'},
            'jar': {'options': ["jars", "jar"], 'type': 'unit'},
            'slice': {'options': ["slices", "slice"], 'type': 'unit'},
            'package': {'options': ["package", "packages"], 'type': 'unit'},
            'stalk': {'options': ["stalk", "stalks"], 'type': 'unit'},
            'stick': {'options': ["stick", "sticks"], 'type': 'unit'},
            'whole': {'options': ["whole"], 'type': 'unit'},
            'can': {'options': ["cans", "can"], 'type': 'volume'},
            'scoop': {'options': ["scoop", "scoops"], 'type': 'volume'},
            'dollup': {'options': ["dollop", "dollops"], 'type': 'volume'},
            'in': {'options': ["inch", "inches", "in."], 'type': 'length'}
        }
        self.volume_unit_df = pd.DataFrame({'teaspoon': [1.0],
                                              'cup': [0.0208333],
                                              'gallon': [0.00130208],
                                              'quart': [0.00520833],
                                              'pint': [0.0104167],
                                              'fl_oz': [0.166667],
                                              'tablespoon': [0.333333],
                                              'liter': [0.00492892],
                                              'milliliter': [4.92892],
                                              'pinch': [0.25],
                                              'dash': [0.125],
                                              'touch': [0.0625],
                                              'handful': [0.0104167],
                                              'bunch': [0.0104167],
                                              'to_taste': [0.125],
                                              'drizzle': [2.0],
                                              'sprinkle': [0.0625],
                                              'garnish': [0.0104167],
                                              'scoop': [0.02],
                                              'dollup': [0.4],
                                              })
        self.weight_unit_df = pd.DataFrame({'gram': [1.0],
                                              'ounce': [0.035274],
                                              'pound': [0.00220462],
                                              'milligram': [1000.0],
                                              'kilogram': [0.001]
                                              })

        self.food_size = ["small", "medium", "large", "about"]

    def extract_recipe_dataframe(self, tag, conversion_factor):
        df_temp = self.nutrtion_init.NDB_NO_lookup(tag, filter_list=self.filter_list)
        df_temp = df_temp * float(conversion_factor)
        df_temp_tag = self.nutrtion_init.NDB_NO_lookup(tag, filter_list=['NDB_NO', 'Description', 'Category'])

        return df_temp_tag.join(df_temp)

    def unit_food_conversion(self, recipe_amount, recipe_unit, tag, recipe_ingredient):
        temp_nutritional_df = self.nutrtion_init.NDB_NO_lookup(tag, filter_list=['Measure', 'Weight(g)'])
        nutrition_df_measure = temp_nutritional_df['Measure'].get_values()[0].replace(",", "")
        nutrition_df_measure_list = nutrition_df_measure.split(" ")
        nutrition_df_amount = float(list(filter(None, re.findall(r"([/.0-9]*)", nutrition_df_measure)))[0])

        nutrition_df_weight = temp_nutritional_df['Weight(g)'].get_values()[0]

        nutrition_df_key = ''
        nutrition_df_type = ''
        recipe_key = ''
        recipe_type = ''
        for key in self.food_unit_standard_dictionary.keys():
            temp_df_unit_list = list(set(nutrition_df_measure_list).intersection(self.food_unit_standard_dictionary[key]['options']))

            if len(temp_df_unit_list) > 0 and nutrition_df_key == '':
                nutrition_df_key = key
                nutrition_df_type = self.food_unit_standard_dictionary[key]['type']

            if recipe_unit in self.food_unit_standard_dictionary[key]['options'] and recipe_key == '':
                recipe_key = key
                recipe_type = self.food_unit_standard_dictionary[key]['type']

        if nutrition_df_key == '':
            nutrition_df_key = 'whole'
            nutrition_df_type = 'unit'



        if recipe_type == 'weight':
            temp_recipe_g = float(recipe_amount) * (float(self.weight_unit_df['gram'].get_values()[0]) / float(self.weight_unit_df[recipe_key].get_values()[0]))
            conversion_factor = temp_recipe_g / nutrition_df_weight
            # self.weight_unit_df[nutrition_df_key].get_values()[0] / self.weight_unit_df[recipe_key].get_values()[0]
        elif recipe_type == 'volume' and recipe_type == nutrition_df_type:
            conversion_factor = (float(recipe_amount) * float(self.volume_unit_df[nutrition_df_key].get_values()[0])) / (float(nutrition_df_amount) * float(self.volume_unit_df[recipe_key].get_values()[0]))
        else:
            conversion_factor = self.ambiguous_df_look_up(tag, recipe_ingredient, recipe_key)

        return conversion_factor

    def ambiguous_df_look_up(self, tag, recipe_ingredient, recipe_key):
        temp_nutritional_df = self.nutrtion_init.NDB_NO_lookup(tag, filter_list=['Measure', 'Weight(g)'])

        filtered_ambiguous_df = self.ambiguous_df[self.ambiguous_df['NDB_NO'] == "\"{}\"".format(tag.strip('"'))]
        filtered_ambiguous_df = filtered_ambiguous_df.reset_index()

        recipe_ingredient_unit_dict = self.extact_unit_from_recipe(recipe_ingredient)
        amount_recipe, unit_recip = self.extact_number_from_recipe(recipe_ingredient, recipe_ingredient_unit_dict)
        unit_recip = recipe_key

        temp_recipe_ingredient = str(recipe_ingredient.replace(str(amount_recipe), "").lstrip(" "))

        itr = 0
        matching_levenstein_ratio_list = []

        if len(filtered_ambiguous_df) > 1:
            while itr < len(filtered_ambiguous_df):
                temp_ambiguos_ingredient = filtered_ambiguous_df.loc[itr, 'Ingredient']
                temp_ambiguos_ingredient = re.sub(r"([/.0-9]*)", "", temp_ambiguos_ingredient).lstrip(" ")

                matching_levenstein_ratio_list.append(Levenshtein.ratio(temp_ambiguos_ingredient, temp_recipe_ingredient))
                itr += 1

            levenstein_index = matching_levenstein_ratio_list.index(max(matching_levenstein_ratio_list))
        elif len(filtered_ambiguous_df) == 1:
            levenstein_index = 0
        else:
            print("\t\tERROR", recipe_ingredient, tag, unit_recip, self.food_unit_standard_dictionary[unit_recip]['type'])
            levenstein_index = 0

        if self.food_unit_standard_dictionary[unit_recip]['type'] == 'weight':
            temp_recipe_g = float(amount_recipe) * float(self.weight_unit_df['gram'])
            conversion_factor = float(temp_recipe_g) / float(temp_nutritional_df['Weight(g)'].get_values()[0])

        elif self.food_unit_standard_dictionary[unit_recip]['type'] == 'volume':
            temp_recipe_g = (float(amount_recipe) * float(self.volume_unit_df['cup'].get_values()[0])) / (float(filtered_ambiguous_df.loc[levenstein_index, 'cups']) * float(self.volume_unit_df[unit_recip].get_values()[0]))
            conversion_factor = (float(temp_recipe_g) * float(filtered_ambiguous_df.loc[levenstein_index, 'grams'])) / float(temp_nutritional_df['Weight(g)'].get_values()[0])

        elif self.food_unit_standard_dictionary[unit_recip]['type'] == 'unit':
            temp_recipe_g = float(amount_recipe) * float(filtered_ambiguous_df.loc[levenstein_index, 'grams'])
            conversion_factor = float(temp_recipe_g) / float(temp_nutritional_df['Weight(g)'].get_values()[0])

        return conversion_factor

    def extact_unit_from_recipe(self, ingredient):
        unit_list_all = []
        for key in self.food_unit_standard_dictionary:
            for alt_name in self.food_unit_standard_dictionary[key]['options']:
                unit_list_all.append(alt_name)

        ingredient_split = ingredient.split("-")
        ingredient_split = " ".join(ingredient_split)
        ingredient_split = ingredient_split.split(" ")


        unit_list = list(set(unit_list_all).intersection(ingredient_split))

        food_unit_dict = {}
        if len(unit_list) >= 1:
            for unit in unit_list:
                food_unit_dict[ingredient_split.index(unit)] = unit

        return food_unit_dict

    def extact_number_from_recipe(self, ingredient, food_unit_dict):
        ingredient_split = ingredient.split("-")
        ingredient_split = " ".join(ingredient_split)
        ingredient_split = ingredient_split.strip("'").strip('"').split(" ")

        initial_itr = 0
        while initial_itr < len(ingredient_split):
            if '/' in ingredient_split[initial_itr]:
                try:
                    top = ingredient_split[initial_itr].split('/')[0]
                    bot = ingredient_split[initial_itr].split('/')[-1]
                    ingredient_split[initial_itr] = str(float(top) / float(bot))
                except:
                    pass
            initial_itr += 1

        ingredient_split = " ".join(ingredient_split)

        amount_list = list(filter(None, re.findall(r"([/.0-9]*)", ingredient_split)))

        food_amount_dict = {}
        if len(amount_list) >= 1:
            for amount in amount_list:
                if not amount == '.':
                    food_amount_dict[ingredient_split.index(amount)] = amount

        amount_key_list = list(food_amount_dict.keys())
        unit_key_list = list(food_unit_dict.keys())

        if len(amount_key_list) == 1 and len(unit_key_list) == 1:
            amount = float(food_amount_dict[amount_key_list[0]])
            unit = food_unit_dict[unit_key_list[0]]

        elif len(amount_key_list) > len(unit_key_list) or len(amount_key_list) == len(unit_key_list):
            if len(unit_key_list) == 1:
                unit = food_unit_dict[unit_key_list[0]]
            else:
                itr = 0
                while itr < len(amount_key_list) - 1:
                    if amount_key_list[itr] == amount_key_list[itr + 1] - 1 and amount_key_list[itr + 1] + 1 in unit_key_list:
                        amount = float(food_amount_dict[amount_key_list[itr]]) * float(food_amount_dict[amount_key_list[itr + 1]])
                        unit = food_unit_dict[unit_key_list[itr + 2]]
                    elif min(amount_key_list) == min(unit_key_list) - 1:
                        amount = float(food_amount_dict[min(amount_key_list)])
                        unit = food_unit_dict[min(unit_key_list)]
                    else:
                        amount = float(food_amount_dict[min(amount_key_list)])
                        unit = food_unit_dict[unit_key_list[min(unit_key_list)]]
                    itr += 1

        elif len(amount_key_list) < len(unit_key_list):
            if len(amount_key_list) == 1:
                amount = float(food_amount_dict[amount_key_list[0]])
                unit = food_unit_dict[amount_key_list[0] + 1]
            else:
                itr = 0
                while itr < len(unit_key_list) - 1:
                    if min(amount_key_list) == min(unit_key_list) - 1:
                        amount = float(food_amount_dict[min(amount_key_list)])
                        unit = food_unit_dict[unit_key_list[min(unit_key_list)]]
                    else:
                        amount = float(food_amount_dict[min(amount_key_list)])
                        unit = food_unit_dict[min(unit_key_list)]
                    itr += 1

        return amount, unit

    def recipe_list_to_conversion_factor_list(self, recipe_id, **kwargs):
        if kwargs:
            temp_dict = kwargs['dict']
            # print(temp_dict)
            # print recipe_id, temp_dict[recipe_id]['name']
            itr = 0
            df_list = []
            while itr < len(temp_dict[recipe_id]['ingredients']):
                try:
                    if temp_dict[recipe_id]['ingredients'][itr] and temp_dict[recipe_id]['NDB_NO_tags'][itr] != 'np.nan' and temp_dict[recipe_id]['NDB_NO_tags'][itr] != '':
                        food_unit_dict = self.extact_unit_from_recipe(temp_dict[recipe_id]['ingredients'][itr])
                        amount, unit = self.extact_number_from_recipe(temp_dict[recipe_id]['ingredients'][itr], food_unit_dict)
                        conversion_factor = self.unit_food_conversion(amount, unit, temp_dict[recipe_id]['NDB_NO_tags'][itr], temp_dict[recipe_id]['ingredients'][itr])

                        if conversion_factor != 'LOOKUP DATABASE':
                            df_temp = self.extract_recipe_dataframe(temp_dict[recipe_id]['NDB_NO_tags'][itr], conversion_factor)
                            df_list.append(df_temp)

                    itr += 1
                except:
                    print("FAILED ingredient:", temp_dict[recipe_id]['ingredients'][itr])
                    conversion_factor = 0
                    df_temp = self.extract_recipe_dataframe(temp_dict[recipe_id]['NDB_NO_tags'][itr], conversion_factor)
                    df_list.append(df_temp)
                    itr += 1

            recipe_master_df = pd.concat(df_list)
        else:
            # print recipe_id, self.recipe_clean[recipe_id]['name']
            itr = 0
            df_list = []
            while itr < len(self.recipe_clean[recipe_id]['ingredients']):
                if self.recipe_clean[recipe_id]['ingredients'][itr] and self.recipe_clean[recipe_id]['NDB_NO_tags'][itr] != 'np.nan' and self.recipe_clean[recipe_id]['NDB_NO_tags'][itr] != '':
                    food_unit_dict = self.extact_unit_from_recipe(self.recipe_clean[recipe_id]['ingredients'][itr])
                    amount, unit = self.extact_number_from_recipe(self.recipe_clean[recipe_id]['ingredients'][itr], food_unit_dict)


                    conversion_factor = self.unit_food_conversion(amount, unit, self.recipe_clean[recipe_id]['NDB_NO_tags'][itr], self.recipe_clean[recipe_id]['ingredients'][itr])

                    if conversion_factor != 'LOOKUP DATABASE':
                        df_temp = self.extract_recipe_dataframe(self.recipe_clean[recipe_id]['NDB_NO_tags'][itr], conversion_factor)
                        df_list.append(df_temp)

                itr += 1
            recipe_master_df = pd.concat(df_list)

        return recipe_master_df

    def recipe_alternitive_create(self, replace_tag, tag_list, new_recipe_dict):

        for key in new_recipe_dict.keys():
            if '_ALT_' not in key:
                orig_recipe_dict_names = key

        index_to_replace = new_recipe_dict[orig_recipe_dict_names]['NDB_NO_tags'].index("\"{}\"".format(replace_tag.strip('"')))
        original_NDB_list = new_recipe_dict[orig_recipe_dict_names]['NDB_NO_tags'][:]

        recipe_id_list = [orig_recipe_dict_names]
        for i in range(len(tag_list)):
            recipe_name_itr = len(new_recipe_dict.keys())
            new_dict_name = orig_recipe_dict_names + '_ALT_' + str(recipe_name_itr)
            recipe_id_list.append(new_dict_name)
            new_recipe_dict[new_dict_name] = new_recipe_dict[key].copy()

            temp_NDB_list = original_NDB_list[:]
            temp_NDB_list[index_to_replace] = tag_list[i]

            new_recipe_dict[new_dict_name]['NDB_NO_tags'] = temp_NDB_list
            new_recipe_dict[new_dict_name]['name'] = str(new_recipe_dict[orig_recipe_dict_names]['name']) + ' ALT_' + str(recipe_name_itr)


        return new_recipe_dict
