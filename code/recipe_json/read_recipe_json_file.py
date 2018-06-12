import json
import pandas as pd
import numpy as np
import random
import os

### NEED TO UPDATE LOCATION OF FILE###
# path = 'C:/Users/mgruz/Desktop/w210/data/recipe/recipe_all.json'
# If you run this script from top of git directory w210_capstone and data folder
# is one folder up (just outside of github)
path = os.path.split(os.getcwd())[0]+'/data/recipe/recipe_all.json'
####

with open(path) as f:
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
itr = 0
for recipe_id in mike_list[0:2]:
    print 'List itr=', itr
    print 'id =', data[recipe_id]['id']
    print 'name =', data[recipe_id]['name']
    print 'ingredients:'
    for ingredients in data[recipe_id]['ingredients']:
        print '\t', ingredients
    print "\n"
    raw_input('Hit enter to continue')
    print "\n"
    itr += 1
