import json
from collections import Counter
import networkx as nx
import matplotlib.pyplot as plt
import pylab
from rootseller import nutrtion

class Research(object):
    def __init__(self):
        with open('C:/Users/pa351d/Desktop/w210/data/recipe/recipe_clean_USE.json') as f:
            self.recipe_clean = json.load(f)


    def make_social_network_dict(self):
        network_dict = {}
        recipe_keys_list = list(self.recipe_clean.keys())[:10]

        # for key in recipe_keys_list:
        for key in self.recipe_clean.keys():
            tag_list = self.recipe_clean[key]['NDB_NO_tags'][:]
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

research_init = Research()
social_food_dict = research_init.make_social_network_dict()
nutrtion_init = nutrtion.Nutrition()

label_dict = {}
G=nx.Graph()
for key in social_food_dict.keys():
    label_dict[key] = nutrtion_init.NDB_NO_lookup(key, filter_list='Description').get_values()[0]
    for sub_key in social_food_dict[key].keys():
        try:
            label_dict[sub_key] = nutrtion_init.NDB_NO_lookup(sub_key, filter_list='Description').get_values()[0]
        except:
            print sub_key

for key in label_dict.keys():
    print key, label_dict[key]
    G.add_node(label_dict[key])

for key in social_food_dict.keys():
    for sub_key in social_food_dict[key].keys():
        G.add_edge(label_dict[key], label_dict[sub_key], weight=social_food_dict[key][sub_key])
#
edge_labels = dict([((u, v,), d['weight']) for u, v, d in G.edges(data=True)])
pos = nx.spring_layout(G)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
nx.draw(G, pos)
# nx.draw(G, pos, labels=label_dict, with_labels=True)
# pylab.show()
#
nx.write_gexf(G, 'test.gexf')
