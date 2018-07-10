import seaborn as sns
import numpy as np

class Plots(object):
    def __init__(self, df_list, profile):
        self.df_list = df_list
        self.profile = profile

    def radar_plot(self, recipe_name):
        fig = sns.plt.figure()
        ax_macro = fig.add_subplot(121, polar=True)
        ax_micro = fig.add_subplot(122, polar=True)

        color_list = ['red', 'blue', 'green', 'yellow', 'orange']
        itr = 0
        legend_list = []
        for df in self.df_list:
            labels_micro = np.array(self.profile.micro_label_list)
            data_micro = df.loc[:, self.profile.micro_list].sum()
            data_micro = data_micro / self.profile.profile_micro_filtered_df
            data_micro = data_micro.get_values()[0]
            angles_micro = np.linspace(0, 2 * np.pi, len(labels_micro), endpoint=False)
            data_micro = np.concatenate((data_micro, [data_micro[0]]))
            angles_micro = np.concatenate((angles_micro, [angles_micro[0]]))

            labels_macro = np.array(self.profile.macro_label_list)
            data_macro = df.loc[:, self.profile.macro_list]

            data_macro['unsaturated_fat'] = data_macro['Fatty acids, total monounsaturated (g)'] + data_macro['Fatty acids, total polyunsaturated (g)'] + data_macro['Fatty acids, total trans (g)']
            del data_macro['Fatty acids, total monounsaturated (g)']
            del data_macro['Fatty acids, total polyunsaturated (g)']
            del data_macro['Fatty acids, total trans (g)']

            data_macro = data_macro[['Energy (kcal)', 'Total lipid (fat) (g)', 'Carbohydrate, by difference (g)',
                                     'Fiber, total dietary (g)', 'Cholesterol (mg)', 'Fatty acids, total saturated (g)',
                                     'unsaturated_fat', 'Sugars, total (g)', 'Protein (g)']]

            data_macro.columns = self.profile.profile_macro_filtered_df.columns
            data_macro = data_macro.sum()

            data_macro = data_macro / self.profile.profile_macro_filtered_df
            data_macro = data_macro.get_values()[0]
            angles_macro = np.linspace(0, 2 * np.pi, len(labels_macro), endpoint=False)
            data_macro = np.concatenate((data_macro, [data_macro[0]]))
            angles_macro = np.concatenate((angles_macro, [angles_macro[0]]))


            ax_macro.plot(angles_macro, data_macro, 'o-', linewidth=2, color=color_list[itr])
            ax_macro.fill(angles_macro, data_macro, alpha=0.25, color=color_list[itr])
            ax_macro.set_thetagrids(angles_macro * 180/np.pi, labels_macro)
            ax_macro.set_title("Macro Percentage")
            ax_macro.grid(True)

            ax_micro.plot(angles_micro, data_micro, 'o-', linewidth=2, color=color_list[itr])
            ax_micro.fill(angles_micro, data_micro, alpha=0.25, color=color_list[itr])
            ax_micro.set_thetagrids(angles_micro * 180/np.pi, labels_micro)
            ax_micro.set_title("Micro Percentage")
            ax_micro.grid(True)

            itr += 1

        fig.legend(handles=ax_micro.lines[::], labels=recipe_name)
        ax_macro.plot(angles_macro, np.asarray([1.0] * int(len(labels_macro) + 1)), '--', linewidth=2, color='black')
        ax_micro.plot(angles_micro, np.asarray([1.0] * int(len(labels_micro) + 1)), '--', linewidth=2, color='black')


        fig.savefig('test_radar')


    def stacked_barplot(self, itr, recipe_list):
        df_temp = self.df_list[itr]

        df_temp['unsaturated_fat'] = df_temp['Fatty acids, total monounsaturated (g)'] + df_temp['Fatty acids, total polyunsaturated (g)'] + df_temp['Fatty acids, total trans (g)']
        del df_temp['Fatty acids, total monounsaturated (g)']
        del df_temp['Fatty acids, total polyunsaturated (g)']
        del df_temp['Fatty acids, total trans (g)']

        df_temp.columns = ['NDB_NO', 'Description', 'Category'] + self.profile.micro_label_list + self.profile.macro_label_list
        df_string = df_temp[['NDB_NO', 'Description', 'Category']]
        df_numbers = df_temp[self.profile.macro_label_list + self.profile.micro_label_list]

        df_numbers = df_numbers / df_numbers.sum()
        df_temp = df_string[['Description']].join(df_numbers)
        stacked_plot = df_temp.set_index('Description').T.plot(kind='bar', stacked=True, colormap='Paired')
        patches, labels = stacked_plot.get_legend_handles_labels()
        stacked_plot.legend(patches, labels, bbox_to_anchor=(1.5, 1.0))


        fig = stacked_plot.get_figure()
        fig.suptitle(recipe_list[itr])
        # fig.tight_layout()
        fig.savefig('test_stacked_barplot', bbox_inches='tight')
