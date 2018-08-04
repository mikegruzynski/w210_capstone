import pandas as pd
import numpy as np
from app.user_profile_support.rootseller import rootprofile, recipes, models

# Run the Pantry Suggetion code
def get_pantry_suggetsions(user_profile_data, ingredient_list, num_suggested_recipes=5):
    # Input: list of pantry items and nutriotial Goals
    # Output: List of x recipe ID

    # initlize user needs:
    profile_init = rootprofile.UserProfile(user_profile_data)
    recipe_init = recipes.Recipes(profile_init)
    model_init = models.Models(recipe_init)


    ## Virtual Pantry to recipe suggestion
    # ingredient_list = ['12 large egg', '12 oz mayonnaise', '12 oz BBQ Sauce', '24 oz mustard', '6 skinless chicken breast',
    #                    '12 salmon burgers', '12 pita', '2 zucchini', '4 onions', '1 pound mushrooms',
    #                    '12 cups lettuce', '24 beer', '1 whole duck', '4 oranges', '2 potatoes', '2 red peppers',
    #                    '4 pounds white rice', '48 oz peanut butter', '6 sausage', '4 pounds ham', '1 cauliflower',
    #                    '6 sticks butter', '12 cups sugar', '12 brown sugar', 'water', '1 whole lemon', '0.25 cup lemon juice',
    #                    '10 whole apples', '1 tomato', '0.25 cup Lime juice', '1 bottle rum', '12 egg whites', '1 whole garlic']


    pantry_list = []
    pantry_tag_list = []
    for ingredient in ingredient_list:
        ingredient_filtered = model_init.transform_data_for_tokenizer(ingredient)
        tokens = model_init.tokenizer.texts_to_matrix([ingredient_filtered])
        prediction_key = str(model_init.loaded_model.predict(np.array(tokens)).argsort()[0][-1:][::-1][0])
        for item in model_init.NDB_tag_unique_unique_dict.items():
            if item[1] == int(prediction_key):
                tag_key = item[0]
                break
        prediction_value = recipe_init.nutrition_init.NDB_NO_lookup(tag_key, filter_list=['Description']).get_values()[0][0]
        pantry_tag_list.append(tag_key)

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

    # create list of recipe ids
    recipe_ids = df.recipe_id.values[:num_suggested_recipes]
    return recipe_ids
