import json
from collections import Counter
import networkx as nx
import matplotlib.pyplot as plt
import pylab
from rootseller import nutrtion
from rootseller import recipes

class Research(object):
    def __init__(self):
        try:
            with open('C:/Users/mgruz/Desktop/w210/data/recipe/recipe_clean_USE.json') as f:
                self.recipe_clean = json.load(f)
        except:
            with open('C:/Users/pa351d/Desktop/w210/data/recipe/recipe_clean_USE.json') as f:
                self.recipe_clean = json.load(f)

        self.nutrtion_init = nutrtion.Nutrition()

    def make_social_network_dict(self):
        network_dict = {}
        # recipe_keys_list = list(self.recipe_clean.keys())[:10]/
        # for key in recipe_keys_list:
        for key in self.recipe_clean.keys():
            tag_list = self.recipe_clean[key]['NDB_NO_tags'][:]
            for i in range(len(tag_list)):
                if tag_list[i] == 'np.nan':
                    tag_list[i] = ''
            tag_list = filter(None, tag_list)
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
            label_dict[key] = self.nutrtion_init.NDB_NO_lookup(key, filter_list='Description').get_values()[0]
            for sub_key in social_food_dict[key].keys():
                try:
                    label_dict[sub_key] = self.nutrtion_init.NDB_NO_lookup(sub_key, filter_list='Description').get_values()[0]
                except:
                    print 'ERROR', sub_key
        for key in label_dict.keys():
            print key, label_dict[key]
            G.add_node(label_dict[key])
        for key in social_food_dict.keys():
            for sub_key in social_food_dict[key].keys():
                G.add_edge(label_dict[key], label_dict[sub_key], weight=social_food_dict[key][sub_key])
        edge_labels = dict([((u, v,), d['weight']) for u, v, d in G.edges(data=True)])
        pos = nx.spring_layout(G)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        nx.draw(G, pos)
        nx.write_gexf(G, 'test.gexf')
#
research_init = Research()
social_food_dict = research_init.make_social_network_dict()
research_init.build_recipe_graph(social_food_dict)


