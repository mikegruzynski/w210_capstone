from rootseller import rootprofile
from rootseller import recipes
from rootseller import research
from rootseller import models
from rootseller import visualizations
import linecache
import sys
import pandas as pd
import numpy as np
import itertools
import warnings
warnings.filterwarnings('ignore')
warnings.filterwarnings("ignore", category=DeprecationWarning)


profile_init = rootprofile.UserProfile('mikegruzynski')
recipe_init = recipes.Recipes(profile_init)
research_init = research.Research(profile_init)
GA = models.GA()
model_init = models.Models(recipe_init)

profile_init.profile_micro_filtered_df
profile_init.micro_list
profile_init.micro_label_list

# recipe_itr = 0
# # # list_keys = list(recipe_init.recipe_clean.keys())
# # # list_keys = ['RECIPE_48743', 'RECIPE_9117', 'RECIPE_14972', 'RECIPE_78461', 'RECIPE_25618']
# list_keys = ['RECIPE_48743', 'RECIPE_9117', 'RECIPE_78461']
# # list_keys = ['RECIPE_9117']
# df_list = []
# df_summed_list = []
# recipe_id_list = []
# name_list = []
# for recipe in list_keys:
#     print("*******************************", "Recipe Itr: ", recipe_itr, "Out of: ", len(list_keys) - 1, recipe)
#     try:
#         temp_recipe_df = recipe_init.recipe_list_to_conversion_factor_list(recipe)
#         df_list.append(temp_recipe_df)
#         df_summed_list.append(temp_recipe_df.loc[:, profile_init.macro_list + profile_init.micro_list].sum().to_frame())
#         name_list.append(recipe_init.recipe_clean[recipe]['name'])
#         recipe_id_list.append(recipe)
#     except Exception as e:
#         print("/t******** FAILED: Recipe Itr: ", recipe_itr, recipe)
#         print('/t/t', e)
#         exc_type, exc_obj, tb = sys.exc_info()
#         f = tb.tb_frame
#         lineno = tb.tb_lineno
#         filename = f.f_code.co_filename
#         linecache.checkcache(filename)
#         line = linecache.getline(filename, lineno, f.f_globals)
#         print('/t/tEXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
#         print('/n')
#     recipe_itr += 1
#
# ## SMASH Files together for optimization map
# print(len(df_summed_list))
# df = pd.concat(df_summed_list, axis=1)
# df = df.T.reset_index(drop=True)
# se = pd.Series(name_list)
# df['recipe_name'] = se.values
# se2 = pd.Series(recipe_id_list)
# df['recipe_id'] = se2.values
# print(df)
#
# new_columns = profile_init.init_macro.convert_labels_to_pretty_labels(df.columns)
# new_columns = profile_init.init_micro.convert_labels_to_pretty_labels(new_columns)
# df.columns = new_columns
# df = profile_init.init_macro.add_unsaturated_fat_columns(df)
# print(df)
#
# print(pd.concat(df_list))
# #
# # ## Visualizations for meal plans
# visualizations.Plots(df_list, profile_init).radar_plot_recipe(name_list, 'test_radar_plot')
# visualizations.Plots(df_list, profile_init).stacked_barplot(0, name_list, 'test_stacked_barplot')
# visualizations.Plots(df_list, profile_init).bar_plot_recipe(name_list, 'test_barplot')
#
# print()
# print('***************NEXT FEATURE**************************')
# print()
#
#
#
# # Single food replacement based on macros
# # recipe_id = 'RECIPE_48743'
# recipe_id = 'RECIPE_25618'
# print(recipe_init.recipe_list_to_conversion_factor_list(recipe_id)[['Description', 'NDB_NO']])
# raw_input_return = input("Select items to replace:")
#
# temp_recipe_dict = {}
# temp_recipe_dict[recipe_id] = recipe_init.recipe_clean[recipe_id].copy()
#
# if raw_input_return:
#
#     replacement_key_dict = {1:  'Baked',
#                             2:  'Beef',
#                             3:  'Beverages',
#                             4:  'Breakfast_Cereals',
#                             5:  'Cereal_Grains_and_Pasta',
#                             6:  'Dairy_and_Egg',
#                             7:  'Fats_and_Oils',
#                             8:  'Finfish_and_Shellfish',
#                             9:  'Fruits_and_Fruit_Juices',
#                             10: 'Lamb_Veal_and_Game',
#                             11: 'Legumes_and_Legume',
#                             12: 'Nut_and_Seed',
#                             13: 'Pork',
#                             14: 'Poultry',
#                             15: 'Sausages_and_Luncheon_Meats',
#                             16: 'Soups_Sauces_and_Gravies',
#                             17: 'Spices_and_Herbs',
#                             18: 'Sweets',
#                             19: 'Vegetables_and_Vegetable'}
#
#     split_raw_return = raw_input_return.split(",")
#     # "05097":8,"44005":7
#
#     master_tag_list = []
#     replace_list = []
#     for replacement in split_raw_return:
#         replacement_ndb_tag = replacement.split(":")[0].lstrip(" ")
#         replacement_category_key = int(replacement.split(":")[-1].strip("'").strip('"'))
#         tag_list = research_init.macro_space_distance_top_n(3, replacement_ndb_tag, [replacement_key_dict[replacement_category_key]])
#         # new_recipe_dict = recipe_init.recipe_alternitive_create(replacement_ndb_tag, tag_list, temp_recipe_dict)
#         replace_list.append(replacement_ndb_tag)
#         master_tag_list.append(tag_list)
#
#     iterable_list = list(itertools.product(*master_tag_list))
#     new_recipe_dict = recipe_init.recipe_alternitive_iter_create(replace_list, iterable_list, temp_recipe_dict)
#
#
#
#     temp = recipe_init.recipe_list_to_conversion_factor_list(recipe_id)
#     df_list = []
#     name_list = []
#     for recipe in new_recipe_dict.keys():
#         temp_recipe_df = recipe_init.recipe_list_to_conversion_factor_list(recipe, dict=new_recipe_dict)
#         df_list.append(temp_recipe_df)
#         name_list.append(new_recipe_dict[recipe]['name'])
#     visualizations.Plots(df_list, profile_init).bar_plot_recipe(name_list, 'test_replacement_barplot')
#     visualizations.Plots(df_list, profile_init).radar_plot_recipe(name_list, 'test_replacement_radar_plot')


print()
print('***************NEXT FEATURE**************************')
print()



## Play around with some pca stuff and "social network of food"
# social_food_dict = research_init.make_social_network_dict()
# G = research_init.build_recipe_graph(social_food_dict)
# path_df = research_init.shortest_paths_and_weights(G, 'Eggplant, raw', 'Celery, raw', cutoff=2)
# path_itr = 0
# while path_itr < 10:
#     print(path_df.loc[path_itr, 'path'])
#     path_itr += 1

print()
print('***************NEXT FEATURE**************************')
print()


## Genetic Algorithm to get weekly meal plan
label_of_weights = GA.labels
num_generations = 2
meals_per_week = 6
amount_per_population = 30
amount_parents_mating = 10
weekly_diet_amount = (GA.user_df[GA.macro_labels] / 3.0) * meals_per_week
best_index_list, generation_list, best_estimates_list, time_list = GA.AMGA(num_generations, meals_per_week, amount_per_population, amount_parents_mating, weekly_diet_amount)


# label_of_weights = GA.labels
# num_generations = 50
# for i in range(4, 16, 4):
#     for ii in range(8, 40, 4):
#         for iii in range(4, 16, 4):
#             meals_per_week = i
#             amount_per_population = ii
#             amount_parents_mating = iii
#             weekly_diet_amount = (GA.user_df[GA.macro_labels] / 3.0) * meals_per_week
#             best_index_list, generation_list, best_estimates_list, time_list = GA.AMGA(num_generations, meals_per_week, amount_per_population, amount_parents_mating, weekly_diet_amount)
#
#             amga_final_df = pd.DataFrame(best_estimates_list)
#             num_col = len(amga_final_df.columns)
#             se = pd.Series(generation_list)
#             amga_final_df['generation'] = se.values
#             se = pd.Series(time_list)
#             amga_final_df['time'] = se.values
#             se = pd.Series(best_index_list)
#             amga_final_df['best_index'] = se.values
#             amga_final_df.to_csv('C:/Users/mgruz/Desktop/w210/code/rootseller/GA_EDA/meal_plan/meal_plan_df__MPW-{}__APOP-{}__APAR-{}__COL-{}'.format(meals_per_week, amount_per_population, amount_parents_mating, num_col))

print()
print('***************NEXT FEATURE**************************')
print()

## Genetic Algorithm to get weekly meal plan
recipe_id = 'RECIPE_9117'
recipe = recipe_init.recipe_list_to_conversion_factor_list(recipe_id)
new_columns = profile_init.init_macro.convert_labels_to_pretty_labels(recipe.columns)
new_columns = profile_init.init_micro.convert_labels_to_pretty_labels(new_columns)
recipe.columns = new_columns
recipe = profile_init.init_macro.add_unsaturated_fat_columns(recipe)

label_of_weights = GA.labels
num_generations = 30
amount_per_population = 30
amount_parents_mating = 10
daily_diet_amount = (GA.user_df[GA.macro_labels] / 3.0)
GA.AMGA_individual_recipe(num_generations, recipe, amount_per_population, amount_parents_mating, daily_diet_amount)

print()
print('***************NEXT FEATURE**************************')
print()

## Virtual Pantry to recipe suggestion
ingredient_list = ['12 large egg', '12 oz mayonnaise', '12 oz BBQ Sauce', '24 oz mustard', '6 skinless chicken breast',
                   '12 salmon burgers', '12 pita', '2 zucchini', '4 onions', '1 pound mushrooms',
                   '12 cups lettuce', '24 beer', '1 whole duck', '4 oranges', '2 potatoes', '2 red peppers',
                   '4 pounds white rice', '48 oz peanut butter', '6 sausage', '4 pounds ham', '1 cauliflower',
                   '6 sticks butter', '12 cups sugar', '12 brown sugar', 'water', '1 whole lemon', '0.25 cup lemon juice',
                   '10 whole apples', '1 tomato', '0.25 cup Lime juice', '1 bottle rum', '12 egg whites', '1 whole garlic']
pantry_list = []
pantry_tag_list = []
for ingredient in ingredient_list:
    ingredient_filtered = model_init.transform_data_for_tokenizer(ingredient)
    tokens = model_init.tokenizer.texts_to_matrix([ingredient_filtered])
    prediction_key = str(model_init.loaded_model.predict(np.array(tokens)).argsort()[0][-1:][::-1][0])
    prediction_value = recipe_init.nutrition_init.NDB_NO_lookup(model_init.NDB_tag_unique_unique_dict[prediction_key], filter_list=['Description']).get_values()[0][0]
    pantry_list.append(prediction_value)
    pantry_tag_list.append(model_init.NDB_tag_unique_unique_dict[prediction_key])
recipe_id_list = []
percent_overlap_list = []
ingredient_pantry_list = []
recipe_full_list = []
for recipe in recipe_init.recipe_clean.keys():
    temp_recipe_list = []
    itr = 0
    while itr < len(recipe_init.recipe_clean[recipe]["NDB_NO_tags"]):
        try:
            if recipe_init.nutrition_init.NDB_NO_lookup(recipe_init.recipe_clean[recipe]["NDB_NO_tags"][itr], filter_list=['Category']).get_values()[0][0] not in ['Fats_and_Oils', 'Spices_and_Herbs']:
                temp_recipe_list.append(recipe_init.recipe_clean[recipe]["NDB_NO_tags"][itr])
        except:
            pass
        itr += 1

    overlap_list = list(set(temp_recipe_list).intersection(pantry_tag_list))
    amount_overlap = len(overlap_list)
    amount_recipe = len(temp_recipe_list)

    recipe_id_list.append(recipe)
    try:
        percent_overlap_list.append(amount_overlap/amount_recipe)
        ingredient_pantry_list.append(overlap_list)
        recipe_full_list.append(temp_recipe_list)
    except:
        percent_overlap_list.append(0.0)
        ingredient_pantry_list.append([])
        recipe_full_list.append([])

df = pd.DataFrame({'recipe_id': recipe_id_list,
                  'percent_overlap': percent_overlap_list,
                   'ingredient_pantry_list': ingredient_pantry_list,
                   'recipe_full_list': recipe_full_list})

df = df.sort_values(by='percent_overlap', ascending=False).reset_index()[['recipe_id', 'percent_overlap', 'ingredient_pantry_list', 'recipe_full_list']]

for i in range(20):
    print(df.loc[i, 'recipe_id'], df.loc[i, 'percent_overlap'], recipe_init.recipe_clean[df.loc[i, 'recipe_id']]['name'])
    print(recipe_init.recipe_clean[df.loc[i, 'recipe_id']]['ingredients'])
    missing_items = list(set(df.loc[i, 'recipe_full_list']) - set(df.loc[i, 'ingredient_pantry_list']))
    for missing in missing_items:
        print('/t', recipe_init.nutrition_init.NDB_NO_lookup(missing, filter_list=['Description']).get_values()[0][0])
    print()


print()
print('***************END**************************')
print()