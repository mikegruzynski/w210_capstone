from rootseller import rootprofile
from rootseller import recipes
from rootseller import research
from rootseller import visualizations
import linecache
import sys
import pandas as pd

profile_init = rootprofile.UserProfile('mikegruzynski')
recipe_init = recipes.Recipes(profile_init)
research_init = research.Research(profile_init)

recipe_itr = 0
# list_keys = list(recipe_init.recipe_clean.keys())
# list_keys = ['RECIPE_48743', 'RECIPE_9117', 'RECIPE_14972', 'RECIPE_78461', 'RECIPE_25618']
# list_keys = ['RECIPE_48743', 'RECIPE_9117']
list_keys = ['RECIPE_24578', 'RECIPE_60641', 'RECIPE_14063']
df_list = []
df_summed_list = []
recipe_id_list = []
name_list = []
for recipe in list_keys:
    print("*******************************", "Recipe Itr: ", recipe_itr, "Out of: ", len(list_keys) - 1, recipe)
    try:
        temp_recipe_df = recipe_init.recipe_list_to_conversion_factor_list(recipe)
        df_list.append(temp_recipe_df)
        df_summed_list.append(temp_recipe_df.loc[:, profile_init.macro_list + profile_init.micro_list].sum().to_frame())
        name_list.append(recipe_init.recipe_clean[recipe]['name'])
        recipe_id_list.append(recipe)
    except Exception as e:
        print("\t******** FAILED: Recipe Itr: ", recipe_itr, recipe)
        print('\t\t', e)
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        print('\t\tEXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
        print('\n')
    recipe_itr += 1

## SMASH Files together for optimization mapp
print(len(df_summed_list))
df = pd.concat(df_summed_list, axis=1)
df = df.T.reset_index(drop=True)
se = pd.Series(name_list)
df['recipe_name'] = se.values
se2 = pd.Series(recipe_id_list)
df['recipe_id'] = se2.values
print(df[['recipe_id'] + profile_init.macro_list])

## Visualizations for meal plans
visualizations.Plots(df_list, profile_init).radar_plot_recipe(name_list)
visualizations.Plots(df_list, profile_init).stacked_barplot(0, name_list)
visualizations.Plots(df_list, profile_init).bar_plot_recipe(name_list)


## Single food replacement based on macros
recipe_id = 'RECIPE_48743'
print(recipe_init.recipe_list_to_conversion_factor_list(recipe_id)[['Description', 'NDB_NO']])
raw_input_return = input("Select items to replace:")

temp_recipe_dict = {}
temp_recipe_dict[recipe_id] = recipe_init.recipe_clean[recipe_id].copy()

if raw_input_return:
    tag_list = research_init.macro_space_distance_top_n(3, raw_input_return, ['Finfish_and_Shellfish'])
    new_recipe_dict = recipe_init.recipe_alternitive_create(raw_input_return, tag_list, temp_recipe_dict)

    df_list = []
    name_list = []
    for recipe in new_recipe_dict.keys():
        temp_recipe_df = recipe_init.recipe_list_to_conversion_factor_list(recipe, dict=new_recipe_dict)
        df_list.append(temp_recipe_df)
        name_list.append(new_recipe_dict[recipe]['name'])

    visualizations.Plots(df_list, profile_init).stacked_barplot(0, name_list)
    visualizations.Plots(df_list, profile_init).radar_plot_recipe(name_list)


## Play around with some pca stuff and "social network of food"
# social_food_dict = research_init.make_social_network_dict()
# G = research_init.build_recipe_graph(social_food_dict)
# path_df = research_init.shortest_paths_and_weights(G, 'Eggplant, raw', 'Celery, raw', cutoff=2)
# pca_df = research_init.pca_space_transformation(profile_init.micro_list + profile_init.macro_list)