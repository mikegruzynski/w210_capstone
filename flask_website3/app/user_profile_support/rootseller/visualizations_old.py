import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import seaborn as sns
import os

class Plots(object):
    def __init__(self, df_list, df, rootprofile):
        self.df_list = df_list
        self.df = df
        self.save_path = 'app/static/images/recipes/'
        self.rootprofile = rootprofile
        self.color_list = ['red', 'blue', 'green', 'yellow', 'orange',
                           'pink', 'aqua', 'lawngreen', 'lemonchiffon', 'khaki',
                           'maroon', 'navy', 'darkgreen', 'y', 'darkgoldenrod']

    def radar_plot_recipe(self, recipe_name):
        fig = plt.figure()

        ax_macro = fig.add_subplot(121, polar=True)
        ax_micro = fig.add_subplot(122, polar=True)

        itr = 0
        legend_list = []
        for df in self.df_list:
            labels_micro = np.array(self.rootprofile.micro_label_list)
            data_micro = df.loc[:, self.rootprofile.micro_list].sum()
            data_micro = data_micro / self.rootprofile.profile_micro_filtered_df
            data_micro = data_micro.get_values()[0]
            angles_micro = np.linspace(0, 2 * np.pi, len(labels_micro), endpoint=False)
            data_micro = np.concatenate((data_micro, [data_micro[0]]))
            angles_micro = np.concatenate((angles_micro, [angles_micro[0]]))

            labels_macro = np.array(self.rootprofile.macro_label_list)
            data_macro = df.loc[:, self.rootprofile.macro_list]

            data_macro['unsaturated_fat'] = data_macro['Fatty acids, total monounsaturated (g)'] + data_macro['Fatty acids, total polyunsaturated (g)'] + data_macro['Fatty acids, total trans (g)']
            del data_macro['Fatty acids, total monounsaturated (g)']
            del data_macro['Fatty acids, total polyunsaturated (g)']
            del data_macro['Fatty acids, total trans (g)']

            data_macro = data_macro[['Energy (kcal)', 'Total lipid (fat) (g)', 'Carbohydrate, by difference (g)',
                                     'Fiber, total dietary (g)', 'Cholesterol (mg)', 'Fatty acids, total saturated (g)',
                                     'unsaturated_fat', 'Sugars, total (g)', 'Protein (g)']]

            data_macro.columns = self.rootprofile.profile_macro_filtered_df.columns
            data_macro = data_macro.sum()

            data_macro = data_macro / self.rootprofile.profile_macro_filtered_df
            data_macro = data_macro.get_values()[0]
            angles_macro = np.linspace(0, 2 * np.pi, len(labels_macro), endpoint=False)
            data_macro = np.concatenate((data_macro, [data_macro[0]]))
            angles_macro = np.concatenate((angles_macro, [angles_macro[0]]))

            ax_macro.plot(angles_macro, data_macro, 'o-', linewidth=2, color=self.color_list[itr])
            ax_macro.fill(angles_macro, data_macro, alpha=0.25, color=self.color_list[itr])
            ax_macro.set_thetagrids(angles_macro * 180/np.pi, labels_macro)
            ax_macro.set_title("Macro Percentage")
            ax_macro.grid(True)

            ax_micro.plot(angles_micro, data_micro, 'o-', linewidth=2, color=self.color_list[itr])
            ax_micro.fill(angles_micro, data_micro, alpha=0.25, color=self.color_list[itr])
            ax_micro.set_thetagrids(angles_micro * 180/np.pi, labels_micro)
            ax_micro.set_title("Micro Percentage")
            ax_micro.grid(True)
            itr += 1

        fig.legend(handles=ax_micro.lines[::], labels=recipe_name)
        ax_macro.plot(angles_macro, np.asarray([1.0] * int(len(labels_macro) + 1)), '--', linewidth=2, color='black')
        ax_micro.plot(angles_micro, np.asarray([1.0] * int(len(labels_micro) + 1)), '--', linewidth=2, color='black')
        fig.savefig(self.save_path+'/'+self.df.recipe_id.values[0]+'test_radar')


    def bar_plot_recipe(self, name_list):

        df_new_list = []
        for df in self.df_list:
            data_micro = df.loc[:, self.rootprofile.micro_list].copy()
            data_micro = data_micro.sum() / self.rootprofile.profile_micro_filtered_df
            data_micro.columns = self.rootprofile.micro_label_list

            data_macro = df.loc[:, self.rootprofile.macro_list].copy()
            data_macro['unsaturated_fat'] = data_macro['Fatty acids, total monounsaturated (g)'] + data_macro['Fatty acids, total polyunsaturated (g)'] + data_macro['Fatty acids, total trans (g)']
            del data_macro['Fatty acids, total monounsaturated (g)']
            del data_macro['Fatty acids, total polyunsaturated (g)']
            del data_macro['Fatty acids, total trans (g)']

            data_macro = data_macro[['Energy (kcal)', 'Total lipid (fat) (g)', 'Carbohydrate, by difference (g)',
                                     'Fiber, total dietary (g)', 'Cholesterol (mg)', 'Fatty acids, total saturated (g)',
                                     'unsaturated_fat', 'Sugars, total (g)', 'Protein (g)']]

            data_macro.columns = self.rootprofile.profile_macro_filtered_df.columns
            data_macro = data_macro.sum() / self.rootprofile.profile_macro_filtered_df

            df_out = data_macro.join(data_micro)
            df_new_list.append(df_out)

        df_master = pd.concat(df_new_list)
        df_master = df_master.transpose()
        df_master = df_master.reset_index()
        df_master.columns = ['index'] + name_list

        ax = df_master.plot(x='index', y=name_list, kind="bar", color=self.color_list)
        fig = ax.get_figure()
        fig.savefig(self.save_path+'/'+self.df.recipe_id.values[0]+'test_bargraph_recipe', bbox_inches='tight')


    def stacked_barplot(self, itr, recipe_list):
        df_temp = self.df_list[itr].copy()

        df_temp['unsaturated_fat'] = df_temp['Fatty acids, total monounsaturated (g)'] + df_temp['Fatty acids, total polyunsaturated (g)'] + df_temp['Fatty acids, total trans (g)']
        del df_temp['Fatty acids, total monounsaturated (g)']
        del df_temp['Fatty acids, total polyunsaturated (g)']
        del df_temp['Fatty acids, total trans (g)']

        df_temp.columns = ['NDB_NO', 'Description', 'Category'] + self.rootprofile.micro_label_list + self.rootprofile.macro_label_list
        df_string = df_temp[['NDB_NO', 'Description', 'Category']]
        df_numbers = df_temp[self.rootprofile.macro_label_list + self.rootprofile.micro_label_list]

        df_numbers = df_numbers / df_numbers.sum()
        df_temp = df_string[['Description']].join(df_numbers)
        stacked_plot = df_temp.set_index('Description').T.plot(kind='bar', stacked=True, colormap='Paired')
        patches, labels = stacked_plot.get_legend_handles_labels()
        stacked_plot.legend(patches, labels, bbox_to_anchor=(1.5, 1.0))

        fig = stacked_plot.get_figure()
        fig.suptitle(recipe_list[itr])
        fig.savefig(self.save_path+'/'+self.df.recipe_id.values[0]+'_stacked_plot', bbox_inches='tight')
