import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
warnings.filterwarnings("ignore", category=DeprecationWarning)

class Plots(object):
    def __init__(self, df_list, rootprofile):
        self.df_list = df_list
        self.rootprofile = rootprofile
        self.color_list = ['red', 'blue', 'green', 'yellow', 'orange',
                           'pink', 'aqua', 'lawngreen', 'lemonchiffon', 'khaki',
                           'maroon', 'navy', 'darkgreen', 'y', 'darkgoldenrod']

    def radar_plot_recipe(self, recipe_name, output_file_name):
        fig = plt.figure()

        ax_macro = fig.add_subplot(121, polar=True)
        ax_micro = fig.add_subplot(122, polar=True)
        itr = 0
        legend_list = []
        for df in self.df_list:
            print("RADAR PLOT")
            labels_micro = np.array(self.rootprofile.micro_label_list)
            data_micro = df.loc[:, self.rootprofile.micro_list].sum()
            data_micro = data_micro[self.rootprofile.profile_micro_filtered_df.columns] / self.rootprofile.profile_micro_filtered_df
            data_micro = data_micro.get_values()[0]

            angles_micro = np.linspace(0, 2 * np.pi, len(labels_micro), endpoint=False)
            data_micro = np.concatenate((data_micro, [data_micro[0]]))
            angles_micro = np.concatenate((angles_micro, [angles_micro[0]]))

            labels_macro = np.array(self.rootprofile.macro_label_list)
            data_macro = df.loc[:, self.rootprofile.macro_list]

            print(self.rootprofile.init_macro)
            new_columns = self.rootprofile.init_macro.convert_labels_to_pretty_labels(data_macro.columns)
            data_macro.columns = new_columns
            data_macro = self.rootprofile.init_macro.add_unsaturated_fat_columns(data_macro)
            data_macro = data_macro.sum()

            data_macro = data_macro[self.rootprofile.profile_macro_filtered_df.columns] / self.rootprofile.profile_macro_filtered_df
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
        fig.savefig('test_images/{}'.format(output_file_name))


    def bar_plot_recipe(self, name_list, output_file_name):

        df_new_list = []
        for df in self.df_list:
            data_micro = df.loc[:, self.rootprofile.micro_list].copy()
            data_micro = data_micro[self.rootprofile.profile_micro_filtered_df.columns].sum() / self.rootprofile.profile_micro_filtered_df
            data_micro.columns = self.rootprofile.micro_label_list

            data_macro = df.loc[:, self.rootprofile.macro_list].copy()

            new_columns = self.rootprofile.init_macro.convert_labels_to_pretty_labels(data_macro.columns)
            data_macro.columns = new_columns
            data_macro = self.rootprofile.init_macro.add_unsaturated_fat_columns(data_macro)

            data_macro = data_macro[self.rootprofile.profile_macro_filtered_df.columns].sum() / self.rootprofile.profile_macro_filtered_df

            df_out = data_macro.join(data_micro)
            df_new_list.append(df_out)

        df_master = pd.concat(df_new_list)
        df_master = df_master.transpose()
        df_master = df_master.reset_index()
        df_master.columns = ['index'] + name_list

        ax = df_master.plot(x='index', y=name_list, kind="bar", color=self.color_list)
        ax.plot(df_master.index, [1.0]*len(df_master.index), color='black', linestyle='--', lw=2)

        fig = ax.get_figure()
        fig.savefig('test_images/{}'.format(output_file_name), bbox_inches='tight')


    def stacked_barplot(self, itr, recipe_list, output_file_name):
        df_temp = self.df_list[itr].copy()

        new_columns = self.rootprofile.init_macro.convert_labels_to_pretty_labels(df_temp.columns)
        new_columns = self.rootprofile.init_micro.convert_labels_to_pretty_labels(new_columns)
        df_temp.columns = new_columns
        df_temp = self.rootprofile.init_macro.add_unsaturated_fat_columns(df_temp)

        df_string = df_temp[['NDB_NO', 'Description', 'Category', 'conversion_factor']]
        df_numbers = df_temp[self.rootprofile.macro_label_list + self.rootprofile.micro_label_list]
        df_numbers = df_numbers / df_numbers.sum()[df_numbers.columns]
        df_temp = pd.concat([df_string[['Description']], df_numbers], axis=1)

        stacked_plot = df_temp.set_index('Description').T.plot(kind='bar', stacked=True, colormap='Paired')
        patches, labels = stacked_plot.get_legend_handles_labels()
        stacked_plot.legend(patches, labels, bbox_to_anchor=(1.5, 1.0))

        fig = stacked_plot.get_figure()
        fig.suptitle(recipe_list[itr])
        fig.savefig('test_images/{}'.format(output_file_name), bbox_inches='tight')
