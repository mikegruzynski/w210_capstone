import pandas as pd
import numpy as np
from app.user_profile_support.rootseller import macronutrients
from app.user_profile_support.rootseller import rootprofile
from app.user_profile_support.rootseller import recipes
import math, json
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.utils import PlotlyJSONEncoder


# Create dataframe to feed to plot functions
def create_recipe_rec_df(session, user_meal_plan):
    user_profile_data = pd.read_json(session['data'])
    #// START: initialize for df creation to plot bar/radar plots
    profile_init = rootprofile.UserProfile(user_profile_data)
    recipe_init = recipes.Recipes(profile_init)
    list_keys = user_meal_plan['recipe_id'].get_values()
    #// END

    #// START: loop through each recipe and convert into mathmatical nutrition space
    # return:
    # df_list -> for stacked barplot graph of each recipe individual and what is inside the recipe
    # df_summed_list -> for radar and barplot graph of meal plan
    # recipe_id_list -> used book keeping/linking
    # name_list -> used to help name and make images pretty
    df_list = []
    df_summed_list = []
    recipe_id_list = []
    name_list = []
    recipe_itr = 0
    for recipe in list_keys:
        # print("*******************************", "Recipe Itr: ", recipe_itr, "Out of: ", len(list_keys) - 1, recipe)
        try:
            temp_recipe_df = recipe_init.recipe_list_to_conversion_factor_list(recipe)
            multiplier_normalizer = profile_init.profile_macro_filtered_df['calories'].get_values()[0] / 3.0
            multiplier_normalizer = multiplier_normalizer / temp_recipe_df['Energy (kcal)'].sum()
            for column in [profile_init.macro_list + profile_init.micro_list]:
                temp_recipe_df[column] = temp_recipe_df[column]*multiplier_normalizer
            df_list.append(temp_recipe_df)
            df_summed_list.append(temp_recipe_df.loc[:, profile_init.macro_list + profile_init.micro_list].sum().to_frame())
            name_list.append(recipe_init.recipe_clean[recipe]['name'])
            recipe_id_list.append(recipe)
        except:
            print("FAILED, Recipe concatenation...RECIPE=", recipe)
        recipe_itr += 1

    df = pd.concat(df_summed_list, axis=1)
    df = df.T.reset_index(drop=True)
    se = pd.Series(name_list)
    df['recipe_name'] = se.values
    se2 = pd.Series(recipe_id_list)
    df['recipe_id'] = se2.values
    return df, df_list, df_summed_list, profile_init, name_list


# # Create dataframe to feed for single ingredient sub
# def create_ingredient_sub_df(session, recipe_id, og_nbd_no, new_nbd_no_list):
#     # takes session
#     # take recipe ID of what you are changing
#     # takes original ndb no and 3 possible ingredient subs nbd_nos
#
#     user_profile_data = pd.read_json(session['data'])
#     #// START: initialize for df creation to plot bar/radar plots
#     profile_init = rootprofile.UserProfile(user_profile_data)
#     recipe_init = recipes.Recipes(profile_init)
#
#     list_keys = user_meal_plan['recipe_id'].get_values()
#     #// END
#
#     #// START: loop through each recipe and convert into mathmatical nutrition space
#     # return:
#     # df_list -> for stacked barplot graph of each recipe individual and what is inside the recipe
#     # df_summed_list -> for radar and barplot graph of meal plan
#     # recipe_id_list -> used book keeping/linking
#     # name_list -> used to help name and make images pretty
#     df_list = []
#     df_summed_list = []
#     recipe_id_list = []
#     name_list = []
#     recipe_itr = 0
#     for recipe in list_keys:
#         # print("*******************************", "Recipe Itr: ", recipe_itr, "Out of: ", len(list_keys) - 1, recipe)
#         try:
#             temp_recipe_df = recipe_init.recipe_list_to_conversion_factor_list(recipe)
#             multiplier_normalizer = profile_init.profile_macro_filtered_df['calories'].get_values()[0] / 3.0
#             multiplier_normalizer = multiplier_normalizer / temp_recipe_df['Energy (kcal)'].sum()
#             for column in [profile_init.macro_list + profile_init.micro_list]:
#                 temp_recipe_df[column] = temp_recipe_df[column]*multiplier_normalizer
#             df_list.append(temp_recipe_df)
#             df_summed_list.append(temp_recipe_df.loc[:, profile_init.macro_list + profile_init.micro_list].sum().to_frame())
#             name_list.append(recipe_init.recipe_clean[recipe]['name'])
#             recipe_id_list.append(recipe)
#         except:
#             print("FAILED, Recipe concatenation...RECIPE=", recipe)
#         recipe_itr += 1
#
#     df = pd.concat(df_summed_list, axis=1)
#     df = df.T.reset_index(drop=True)
#     se = pd.Series(name_list)
#     df['recipe_name'] = se.values
#     se2 = pd.Series(recipe_id_list)
#     df['recipe_id'] = se2.values
#     return df, df_list, df_summed_list, profile_init, name_list

# Create Radar and Bar Plots
def full_recipe_rec_plots(df, df_list, df_summed_list, profile_init, session, name_list):
    user_profile_data = pd.read_json(session['data'])

    #// START: initialize lists for plotting information and visualizations
    labels = profile_init.macro_label_list + profile_init.micro_label_list
    recipe_list = df['recipe_id'].get_values()
    recipe_names_list = df['recipe_name'].get_values()
    color_list = ['red', 'blue', 'green', 'yellow', 'orange',
                  'pink', 'aqua', 'lawngreen', 'lemonchiffon', 'khaki',
                  'maroon', 'navy', 'darkgreen', 'gold', 'darkgoldenrod']
    # // END

    # // START: loop through each recipe to get desired information out of them
    trace_bar_list = []
    trace_radar_macro_list = []
    trace_radar_micro_list = []
    master_stack_list = []
    buttons_list = []
    for itr in range(len(recipe_list)):
        #// START: Aggregate information and transform data labels into easily read output labels
        data_micro_raw = df.loc[itr, profile_init.micro_list].to_frame().T.reset_index(drop=True)
        data_micro_normalized = data_micro_raw[profile_init.profile_micro_filtered_df.columns] / profile_init.profile_micro_filtered_df
        data_micro_raw.columns = profile_init.micro_label_list
        data_micro_normalized.columns = profile_init.micro_label_list

        data_macro = df.loc[itr, profile_init.macro_list].to_frame().T.reset_index(drop=True)
        # print(profile_init.init_macro)
        init_macro = macronutrients.Macronutrients(user_profile_data)
        # new_columns = profile_init.macro_list
        new_columns = init_macro.convert_labels_to_pretty_labels(data_macro.columns)
        # new_columns = profile_init.convert_labels_to_pretty_labels(data_macro.columns)
        data_macro.columns = new_columns

        # init_micro = micronutrients.MicroNutrients(self.userprofile_df)
        # data_macro_raw = profile_init.init_macro.add_unsaturated_fat_columns(data_macro)
        data_macro_raw = init_macro.add_unsaturated_fat_columns(data_macro)
        data_macro_normalized = data_macro_raw[
                                    profile_init.profile_macro_filtered_df.columns] / profile_init.profile_macro_filtered_df

        joined_raw_df = data_macro_raw.join(data_micro_raw)
        joined_nomalized_df = data_macro_normalized.join(data_micro_normalized)
        #// END

        # // START: create plotly bar graph for meal plan visualizations
        temp_trace_bar = dict(
            x=labels,
            y=joined_nomalized_df[labels].values.tolist()[0],
            name=recipe_names_list[itr],
            text=joined_raw_df[labels].values.tolist()[0],
            type='bar',
            hoverInfo='text',
            marker=dict(
                color=color_list[itr])
        )
        trace_bar_list.append(temp_trace_bar)
        #// END

        # // START: create plotly radar graph for micro and macro (seperatley) nutrients for meal plan visualizations
        r_macro = data_macro_normalized[profile_init.macro_label_list].values.tolist()[0]
        r_macro.append(r_macro[0])
        theta_macro = profile_init.macro_label_list.copy()
        theta_macro.append(theta_macro[0])

        temp_trace_radar_macro = dict(
            type='scatterpolar',
            r=r_macro,
            theta=theta_macro,
            fill='toself',
            opacity=0.5,
            text=data_macro_raw[profile_init.macro_label_list].values.tolist()[0],
            hoverInfo='text',
            name=recipe_names_list[itr],
            marker=dict(color=color_list[itr],
                        size=10)
        )
        trace_radar_macro_list.append(temp_trace_radar_macro)


        r_micro = data_micro_normalized[profile_init.micro_label_list].values.tolist()[0]
        r_micro.append(r_micro[0])
        theta_micro = profile_init.micro_label_list.copy()
        theta_micro.append(theta_micro[0])

        temp_trace_radar_micro = dict(
            type='scatterpolar',
            r=r_micro,
            theta=theta_micro,
            fill='toself',
            opacity=0.5,
            text=data_micro_raw[profile_init.micro_label_list].values.tolist()[0],
            hoverInfo='text',
            name=recipe_names_list[itr],
            marker=dict(color=color_list[itr],
                        size=10))
        trace_radar_micro_list.append(temp_trace_radar_micro)
        #// END

        # // START: need to loop through unagreggated recipes to get stqcked bar graph of each meal ratio of what goes into the recipe
        recipe_temp_df = df_list[itr].copy()
        recipe_temp_df = recipe_temp_df.reset_index(drop=True)
        recipe_temp_df_micro_fix = recipe_temp_df[profile_init.micro_list]
        recipe_temp_df_micro_fix.columns = profile_init.micro_label_list

        recipe_temp_df_macro_fix = recipe_temp_df[profile_init.macro_list]
        new_columns = init_macro.convert_labels_to_pretty_labels(recipe_temp_df_macro_fix.columns)
        recipe_temp_df_macro_fix.columns = new_columns
        recipe_temp_df_macro_fix = init_macro.add_unsaturated_fat_columns(recipe_temp_df_macro_fix)

        recipe_temp_df_raw = recipe_temp_df_macro_fix.join(recipe_temp_df_micro_fix)
        column_plot_labels = recipe_temp_df_raw.columns
        recipe_temp_df_raw['Description'] = df_list[itr]['Description'].values
        recipe_temp_df_normalized = recipe_temp_df_raw[column_plot_labels] /recipe_temp_df_raw[column_plot_labels].sum()

        t_f_itr = 0
        for index in recipe_temp_df.index:
            temp = dict(
                x=column_plot_labels,
                y=recipe_temp_df_normalized.loc[index, column_plot_labels].values.tolist(),
                type='bar',
                name=recipe_temp_df_raw.loc[index, 'Description'],
                text=recipe_temp_df_raw.loc[index, column_plot_labels].values.tolist(),
                hoverInfo='text')
            t_f_itr += 1

            master_stack_list.append(temp)

        # // START: to filter buy recipe needed to create a list of len(recipe_list) * len(column_plot_labels) * amount of recipes length
        # to filter amount of recipe blocks of length len(recipe_list) * len(column_plot_labels
        true_false_list = np.asarray([False] * (len(recipe_list) * len(column_plot_labels)))
        true_false_list[len(column_plot_labels) * itr: len(column_plot_labels) * itr + len(column_plot_labels) - 1] = True

        buttons_list.append(dict(label=name_list[itr],
                                 method='update',
                                 args=[{'visible': true_false_list.tolist()}]))
        #//END

        itr += 1
        #// END

        # // START: Package the data up to transfer using PlotlyJSONEncoder
    data_meal_plan_bar = trace_bar_list
    layout_meal_plan_bar = go.Layout(xaxis=dict(tickangle=-45), barmode='group')
    # layout_meal_plan_bar = dict(title='Meal Plan')
    dict_meal_plan_bar = dict(data=data_meal_plan_bar, layout=layout_meal_plan_bar)

    data_meal_plan_radar_macro = trace_radar_macro_list
    # layout_meal_plan_radar_macro = go.Layout(polar=dict(radialaxis=dict(visible=True)))
    layout_meal_plan_radar_macro = dict(polar=dict(radialaxis=dict(visible=True)),
                                        legend=dict(x=-.1, y=1.2))
    dict_meal_plan_radar_macro = dict(data=data_meal_plan_radar_macro, layout=layout_meal_plan_radar_macro)

    data_meal_plan_radar_micro = trace_radar_micro_list
    # layout_meal_plan_radar_micro = go.Layout(polar=dict(radialaxis=dict(visible=True)))
    layout_meal_plan_radar_micro = dict(polar=dict(radialaxis=dict(visible=True)),
                                        legend=dict(x=-1, y=1))
    dict_meal_plan_radar_micro = dict(data=data_meal_plan_radar_micro, layout=layout_meal_plan_radar_micro)

    updatemenus_single_stacked_bar = list([dict(active=-1, buttons=buttons_list)])
    data_single_stacked_bar = master_stack_list
    layout_single_stacked_bar = go.Layout(updatemenus=updatemenus_single_stacked_bar,
                                          barmode='stack')
    dict_single_stacked_bar = dict(data=data_single_stacked_bar, layout=layout_single_stacked_bar)

    # graphs = [dict_meal_plan_bar, dict_meal_plan_radar_macro, dict_meal_plan_radar_micro, dict_single_stacked_bar]
    graphs = [dict_meal_plan_bar]
    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]

    graphJSON = json.dumps(graphs, cls=PlotlyJSONEncoder)
    # //END
    # //END

    return ids, graphJSON, data_meal_plan_radar_macro, layout_meal_plan_radar_macro, data_meal_plan_radar_micro, layout_meal_plan_radar_micro
