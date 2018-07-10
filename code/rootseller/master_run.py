from rootseller import profile
from rootseller import recipes
from rootseller import visualizations

profile_init = profile.UserProfile('mikegruzynski')
recipe_init = recipes.Recipes(profile_init)

recipe_itr = 0
# list_keys = list(recipe_init.recipe_clean.keys())
# list_keys = ['RECIPE_48743', 'RECIPE_9117', 'RECIPE_14972', 'RECIPE_78461', 'RECIPE_25618']
list_keys = ['RECIPE_48743', 'RECIPE_9117']
df_list = []
name_list = []
for recipe in list_keys:
    print "*******************************", "Recipe Itr: ", recipe_itr, "Out of: ", len(list_keys) - 1
    temp_recipe_df = recipe_init.recipe_list_to_conversion_factor_list(recipe)
    df_list.append(temp_recipe_df)
    name_list.append(recipe_init.recipe_clean[recipe]['name'])
    recipe_itr += 1

visualizations.Plots(df_list, profile_init).radar_plot(name_list)
visualizations.Plots(df_list, profile_init).stacked_barplot(1, name_list)
