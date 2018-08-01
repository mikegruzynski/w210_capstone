import json
import pandas as pd
from collections import Counter
# import networkx as nx
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from app.user_profile_support.rootseller import nutrition
from app.user_profile_support.rootseller import rootprofile
import warnings
warnings.filterwarnings('ignore')
warnings.filterwarnings("ignore", category=DeprecationWarning)


class Research(object):
    def __init__(self, profile_init):
        path = '/Users/mauracullen/Documents/UCB_MIDS/W210_Capstone/w210_capstone/data/'
        try:
            with open(path + 'recipe/recipe_clean_USE.json') as f:
                self.recipe_clean = json.load(f)
        except:
            with open(path + 'recipe/recipe_clean_USE.json') as f:
                self.recipe_clean = json.load(f)

        try:
            self.df_pca = pd.read_csv(path + 'nutrient/compiled/pca_nutrition_normalized_minmax_df.csv')
        except:
            self.df_pca = None

        self.nutrition_init = nutrition.Nutrition()
        self.profile_init = profile_init

    def make_social_network_dict(self):
        network_dict = {}
        for key in self.recipe_clean.keys():
            tag_list = self.recipe_clean[key]['NDB_NO_tags'][:]
            for i in range(len(tag_list)):
                if tag_list[i] == 'np.nan':
                    tag_list[i] = ''
            tag_list = list(filter(None, tag_list))
            try:
                b = tag_list.index('np.nan')
                del tag_list[b]
            except:
                pass
            itr = 0
            for tag in tag_list:
                if tag not in network_dict.keys():
                    network_dict[tag] = {}
                temp_tag_list = tag_list
                temp_tag_list.remove(tag_list[itr])
                temp_counter_key = Counter(temp_tag_list)
                for value in temp_counter_key:
                    if value not in network_dict[tag]:
                        network_dict[tag][value] = temp_counter_key[value]
                    else:
                        network_dict[tag][value] += temp_counter_key[value]
                itr += 1

        return network_dict

    def build_recipe_graph(self, social_food_dict):
        label_dict = {}
        G = nx.Graph()
        for key in social_food_dict.keys():
            label_dict[key] = self.nutrition_init.NDB_NO_lookup(key, filter_list='Description').get_values()[0]
            for sub_key in social_food_dict[key].keys():
                try:
                    label_dict[sub_key] = self.nutrition_init.NDB_NO_lookup(sub_key, filter_list='Description').get_values()[0]
                except:
                    print('ERROR', sub_key)
        for key in label_dict.keys():
            G.add_node(label_dict[key])
        for key in social_food_dict.keys():
            for sub_key in social_food_dict[key].keys():
                G.add_edge(label_dict[key], label_dict[sub_key], weight=social_food_dict[key][sub_key])
        edge_labels = dict([((u, v,), d['weight']) for u, v, d in G.edges(data=True)])
        pos = nx.spring_layout(G)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        nx.draw(G, pos)
        nx.write_gexf(G, 'test.gexf')
        return G

    def shortest_paths_and_weights(self, G, food_1, food_2, **kwargs):
        if 'cutoff' in kwargs.keys():
            path_list = nx.all_simple_paths(G, food_1, food_2, cutoff=kwargs['cutoff'])
        else:
            path_list = nx.all_simple_paths(G, food_1, food_2, cutoff=2)

        edge_weight_list = []
        edge_list = []
        for edge in (list(path_list)):
            edge_list.append(edge)
            itr = 0
            total_path_weight = 0
            while itr < len(edge) - 1:
                total_path_weight += G.get_edge_data(edge[itr], edge[itr + 1])['weight']
                itr += 1
            edge_weight_list.append(total_path_weight)

        path_df = pd.DataFrame({'edge_weight': edge_weight_list, 'path': edge_list})

        return path_df

    def pca_space_transformation(self, filter_list):
        minmax_scaler = MinMaxScaler()
        pca_method_three = PCA(n_components=3)
        pca_transform_3 = pca_method_three.fit_transform(minmax_scaler.fit_transform(self.nutrition_init.nutritional_normalized_database[filter_list]))
        df_pca = pd.DataFrame(pca_transform_3)
        df_pca.columns = ['PCA_1', 'PCA_2', 'PCA_3']
        df_pca['Category'] = self.nutrition_init.nutritional_normalized_database['Category']
        df_pca['Description'] = self.nutrition_init.nutritional_normalized_database['Description']
        df_pca['NDB_NO'] = self.nutrition_init.nutritional_normalized_database['NDB_NO']

        df_pca.to_csv(path +'nutrient/compiled/pca_nutrition_normalized_minmax_df.csv')

        return df_pca

    def macro_space_distance_top_n(self, n_values, tag, food_category_list):
        minmax_scaler = MinMaxScaler()
        food_to_replace = self.nutrition_init.NDB_NO_lookup_normalized(tag, filter_list=['Description']).get_values()[0][0]
        temp_row = self.nutrition_init.NDB_NO_lookup_normalized(tag, filter_list=self.profile_init.macro_list)
        temp_df = self.nutrition_init.nutritional_normalized_database.copy()

        if 'raw' in food_to_replace.lower():
            temp_df = temp_df[(temp_df['Description'].str.contains('raw'))].reset_index()

        temp_minmax_df = minmax_scaler.fit_transform(temp_df[self.profile_init.macro_list])
        temp_row_minmax = minmax_scaler.transform(temp_row)[0]

        distance_list = []
        for i in range(len(temp_df)):
            distance_list.append(1 - cosine_similarity(temp_row_minmax.reshape(1, -1), temp_minmax_df[i].reshape(1, -1))[0][0])
        se2 = pd.Series(distance_list)
        temp_df['distance'] = se2.values

        tag_list = []
        potential_switches = []
        print(food_category_list)
        for description in food_category_list:
            print("description", description)
            for i in range(n_values):
                tag_list.append(temp_df[temp_df['Category'] == description].sort_values(by=['distance'], ascending=True)['NDB_NO'].get_values()[i])
                print(temp_df[temp_df['Category'] == description].sort_values(by=['distance'], ascending=True)['Description'].get_values()[i])
                potential_switches.append(temp_df[temp_df['Category'] == description].sort_values(by=['distance'], ascending=True)['Description'].get_values()[i])
                print('\t', temp_df[temp_df['Category'] == description].sort_values(by=['distance'], ascending=True)['distance'].get_values()[i], temp_df[temp_df['Category'] == description].sort_values(by=['distance'], ascending=True)['Description'].get_values()[i])
                for ii in self.profile_init.macro_list:
                    normalized_food = temp_row[ii].get_values()[0]
                    normalized_food_next = self.nutrition_init.nutritional_database[self.nutrition_init.nutritional_database['NDB_NO'] == temp_df[temp_df['Category'] == description].sort_values(by=['distance'], ascending=True)['NDB_NO'].get_values()[i]][ii].get_values()[0]
                    # print('\t\t', "{:40s}, {:10f}, {:10f}".format(ii, normalized_food, normalized_food_next))
        print("potential_switches", potential_switches)
        return tag_list, potential_switches
