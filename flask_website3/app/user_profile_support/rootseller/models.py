from keras.models import load_model, model_from_json
import pickle
import re
import numpy as np
from scipy.optimize import linprog
import pandas as pd
# pd.set_option('display.height', 1000)
# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 500)
# pd.set_option('display.width', 10008
from app.user_profile_support.rootseller import recipes
from app.user_profile_support.rootseller import rootprofile

class Models(object):
    def __init__(self, recipe_init):
        path = 'app/static'
        with open(path+'/models/tokenizer.pickle', 'rb') as handle:
            self.tokenizer = pickle.load(handle)
        # load json and create model
        json_file = open(path+'/models/model_simple_nn.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        self.loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        self.loaded_model.load_weights(path+'/models/model_simple_nn_WEIGHTS.h5')

        self.recipe_init = recipe_init

    def transform_data_for_tokenizer(self, recipe_item):
        print("************************************")
        print(recipe_item)
        original = recipe_item.lower()
        original = re.sub(r'/s*(/d+|[./+*-])', '', original)
        original_split = original.split(" ")

        units_of_food_recipe_list = []
        for key in self.recipe_init.food_unit_standard_dictionary:
            print(key)
            for sub_key in self.recipe_init.food_unit_standard_dictionary[key]:
                units_of_food_recipe_list.append(sub_key)

        keep_list = []
        for i in original_split:
            print(i)
            if i not in self.recipe_init.food_size and i not in units_of_food_recipe_list:
                keep_list.append(i)

        original_split = list(filter(None, keep_list))
        new = " ".join(original_split)
        # return new

class GA(object):
    def __init__(self):
        # TODO - Remove dependency on static files
        code_path = 'app/static/csv_files/GA_help'
        self.recipe_df = pd.read_csv(code_path+'/test_GA.csv', encoding="cp1252")
        self.recipe_df_normalized = pd.read_csv(code_path+'/test_GA_normalized.csv', encoding="cp1252")
        self.user_df = pd.read_csv(code_path+'/test_user_df.csv', encoding="cp1252")

        self.labels = ["calories", "fat", "carbohydrate", "fiber", "cholesterol", "saturated_fat",
                       "unsaturated_fat",
                       "sugar", "protein", "Iron, Fe (mg)", "Magnesium, Mg (mg)", "Manganese, Mn (mg)",
                       "Thiamin (mg)",
                       "Vitamin D (D2 + D3) (microg)"]
        self.macro_labels = ["calories", "fat", "carbohydrate", "fiber", "cholesterol", "saturated_fat",
                             "unsaturated_fat",
                             "sugar", "protein"]

    def find_nearest(self, input_array, value):
        input_array = np.asarray(input_array)
        idx = (np.abs(input_array - value)).argmin()
        return idx

    def print_recipe_select_mating_pool(self, user_df, fitness, num_parents):
        df_loss = np.abs((fitness.values - user_df.values) / user_df.values)
        numpy_average_loss = np.average(df_loss, axis=1)
        numpy_average_loss_copy = numpy_average_loss.copy()

        index_list = []
        for parent_num in range(num_parents):
            index = self.find_nearest(numpy_average_loss, 0.0)
            numpy_average_loss[index] = -99999999
            index_list.append(index)

        return index_list, numpy_average_loss_copy

    def recipe_population_fitness(self, meal_plan_population):
        fitness_series_list = []
        for sub_population in meal_plan_population:
            temp_filtered_df = self.recipe_df_normalized[
                self.recipe_df_normalized['recipe_id'].isin(sub_population)]
            temp_filtered_df_sum = temp_filtered_df[self.macro_labels].sum()
            fitness_series_list.append(temp_filtered_df_sum)

        return pd.concat(fitness_series_list, axis=1).T

    def recipe_select_mating_pool(self, user_df, fitness, num_parents):
        df_loss = np.abs((fitness.values - user_df.values) / user_df.values)
        numpy_average_loss = np.average(df_loss, axis=1)

        index_list = []
        for parent_num in range(num_parents):
            index = self.find_nearest(numpy_average_loss, 0.0)
            numpy_average_loss[index] = -99999999
            index_list.append(index)

        return index_list

    def recipe_crossover(self, parents, offspring_size):
        crossover_point = np.uint8(offspring_size[1] / 2)

        offspring_list = []
        for k in range(offspring_size[1]):
            # Index of the first parent to mate.
            parent1_idx = k % parents.shape[0]
            # Index of the second parent to mate.
            parent2_idx = (k + 1) % parents.shape[0]
            # The new offspring will have its first half of its genes taken from the first parent.
            offspring_list.append(
                list(parents[parent1_idx][0:crossover_point]) + list(parents[parent2_idx][crossover_point:]))

        offspring_list = np.asarray(offspring_list)

        return offspring_list

    def recipe_mutation(self, offspring_crossover, user_df, amount_mutations):
        # Mutation changes a single gene in each offspring randomly.
        for sub_population in offspring_crossover:
            for mutation in range(amount_mutations):
                temp_filtered_df = self.recipe_df_normalized[self.recipe_df_normalized['recipe_id'].isin(sub_population)][self.macro_labels]
                temp_filtered_df = temp_filtered_df.reset_index(drop=True)
                temp_filtered_df_sum = temp_filtered_df[self.macro_labels].sum()

                value_differences = (temp_filtered_df_sum.values - user_df.values) / user_df.values
                index_farthest_away_from_zero = np.argmax(abs(value_differences))

                if value_differences[0][index_farthest_away_from_zero] > 0:
                    # find largest value and make smaller
                    recipe_index_to_replace = temp_filtered_df[self.macro_labels[index_farthest_away_from_zero]].idxmax()
                    df_replacement_candidates = self.recipe_df_normalized.copy()
                    temp_value_filter = self.recipe_df_normalized[self.macro_labels[index_farthest_away_from_zero]].mean()
                    try:
                        df_replacement_candidates_filtered = df_replacement_candidates[df_replacement_candidates[self.macro_labels[index_farthest_away_from_zero]] < temp_value_filter]
                        new_recipe = df_replacement_candidates_filtered['recipe_id'].sample(1).get_values()[0]
                        sub_population[recipe_index_to_replace] = new_recipe
                    except:
                        pass


                else:
                    # find smallest value and make larger
                    recipe_index_to_replace = temp_filtered_df[self.macro_labels[index_farthest_away_from_zero]].idxmin()
                    df_replacement_candidates = self.recipe_df_normalized.copy()
                    temp_value_filter = self.recipe_df_normalized[self.macro_labels[index_farthest_away_from_zero]].mean()
                    try:
                        df_replacement_candidates_filtered = df_replacement_candidates[df_replacement_candidates[self.macro_labels[index_farthest_away_from_zero]] > temp_value_filter]
                        new_recipe = df_replacement_candidates_filtered['recipe_id'].sample(1).get_values()[0]
                        sub_population[recipe_index_to_replace] = new_recipe
                    except:
                        pass

        return offspring_crossover

    def AMGA(self, num_generations, meals_per_week, amount_per_population, amount_parents_mating, weekly_diet_amount, ignore_list):
        meal_plan_population = []
        for unit in range(amount_per_population):
            meal_plan_population.append(self.recipe_df_normalized['recipe_id'].sample(meals_per_week).tolist())
        meal_plan_population = np.asarray(meal_plan_population)

        last_best = []
        for generation in range(num_generations):
            # print("Generation : ", generation)
            fitness_recipe = self.recipe_population_fitness(meal_plan_population)

            index = self.recipe_select_mating_pool(weekly_diet_amount, fitness_recipe, amount_parents_mating)
            recipe_parents = meal_plan_population[index]

            recipe_offspring_crossover = self.recipe_crossover(recipe_parents, offspring_size=(amount_per_population - amount_parents_mating, meals_per_week))

            offspring_mutation = self.recipe_mutation(recipe_offspring_crossover, weekly_diet_amount, 10)

            print_best = self.recipe_population_fitness(meal_plan_population)
            print_best_index, df_loss = self.print_recipe_select_mating_pool(weekly_diet_amount, print_best, amount_per_population)
            # print(print_best_index[:5])

            if generation < num_generations - 1:
                meal_plan_population = np.concatenate([recipe_parents, offspring_mutation])

        best_recipe_combo = meal_plan_population[print_best_index[0]]
        # Verify there is no recipe in the ignore list and in teh suggetsion list
        i = 1
        while np.intersect1d(best_recipe_combo, ignore_list):
            best_recipe_combo = meal_plan_population[print_best_index[i]]
            i += 1

        # print(best_recipe_combo)
        # print(self.recipe_population_fitness([meal_plan_population[print_best_index[0]]]))
        # print best_recipe_combo
        # offspring_mutation = self.recipe_mutation([meal_plan_population[print_best_index[0]]], weekly_diet_amount, 10)
        # print offspring_mutation
        # print(weekly_diet_amount)

        return best_recipe_combo, weekly_diet_amount


# # user_init = rootprofile.UserProfile('mikegruzynski')
# recipe_init = recipes.Recipes(user_profile_data)
#
# GA = GA()
# label_of_weights = GA.labels
# num_generations = 10
# meals_per_week = 6
# amount_per_population = 30
# amount_parents_mating = 10
# weekly_diet_amount = (GA.user_df[GA.macro_labels] / 3.0) * meals_per_week
# GA.AMGA(num_generations, meals_per_week, amount_per_population, amount_parents_mating, weekly_diet_amount)


#
# user_init = rootprofile.UserProfile('mikegruzynski')
# recipe_init = recipes.Recipes(user_init)
# models_init = Models(recipe_init)
#
# ingredient = '1 large egg'
# ingredient_filtered = models_init.transform_data_for_tokenizer(ingredient)
# tokens = models_init.tokenizer.texts_to_matrix([ingredient_filtered])
# prediction = models_init.loaded_model.predict(np.array(tokens))
# print(prediction)
