import json
import pandas as pd
import numpy as np
import random

### NEED TO UPDATE LOCATION OF FILE###
with open('C:/Users/mgruz/Desktop/w210/data/recipe/recipe_all.json') as f:
    data = json.load(f)

random.seed(42)
ids = np.unique(data.keys())
random.shuffle(ids)

chunked_list = np.array_split(ids,4)
anjali_list = chunked_list[0]
maura_list = chunked_list[1]
max_list = chunked_list[2]
mike_list = chunked_list[3]

### NEED WHICH USER AND WHAT RANGE IN LIST###
# for recipe_id in anjali_list[0:250]:
# for recipe_id in maura_list[0:250]:
# for recipe_id in max_list[0:250]:
for recipe_id in mike_list[0:2]:
    print 'id =', data[recipe_id]['id']
    print 'name =', data[recipe_id]['name']
    print 'ingredients:'
    for ingredients in data[recipe_id]['ingredients']:
        print '\t', ingredients
    print "\n"
    raw_input('Hit enter to continue')
    print "\n"