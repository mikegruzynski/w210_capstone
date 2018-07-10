from rootseller import profile
from rootseller import recipes

profile_init = profile.UserProfile('mikegruzynski')
recipe_init = recipes.Recipes(profile_init)

recipe_itr = 1
# list_keys = list(recipe_init.recipe_clean.keys())
list_keys = ['RECIPE_48743', 'RECIPE_9117', 'RECIPE_14972', 'RECIPE_78461', 'RECIPE_25618']
for recipe in list_keys:
    print "*******************************", "Recipe Itr: ", recipe_itr, "Out of: ", len(list_keys)
    temp_recipe_df = recipe_init.recipe_list_to_conversion_factor_list(recipe)
    print temp_recipe_df
    print '\n'
    print '\n'
    recipe_itr += 1