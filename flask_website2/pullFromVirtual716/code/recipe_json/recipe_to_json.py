import json

### NEED TO UPDATE LOCATION OF FILE###
recipe_json_file = 'C:/Users/mgruz/Desktop/w210/data/recipe/Recipes.txt'
### NEED TO UPDATE LOCATION OF FILE###

with open(recipe_json_file, 'r') as f:
    file_lines = f.readlines()

recipe_json = {}

itr = 1
ingredients_list = []
instructions_list = []
tags_list = []
while itr < len(file_lines):
    temp_line = file_lines[itr].strip()
    temp_split_line = temp_line.split(",")
    # print itr, len(file_lines)


    if len(temp_split_line) == 3:
        if temp_split_line[0] == 'id':
            temp_id = 'RECIPE_{}'.format(temp_split_line[1])
            recipe_json[temp_id] = {}
            recipe_json[temp_id]['id'] = temp_split_line[1]


            try:
                temp_id_ingredients = 'RECIPE_{}'.format(int(temp_split_line[1]) - 1)
                recipe_json[temp_id_ingredients]['ingredients'] = ingredients_list
                ingredients_list = []

                recipe_json[temp_id_ingredients]['instructions'] = instructions_list
                instructions_list = []

                recipe_json[temp_id_ingredients]['tags'] = tags_list
                tags_list = []
            except:
                'Print recipe not relevant SKIPPING'

        if temp_split_line[0] == 'name':
            temp_id = 'RECIPE_{}'.format(temp_split_line[1])
            recipe_json[temp_id]['name'] = temp_split_line[-1]
            print recipe_json[temp_id]['name']

        if temp_split_line[0] == 'source':
            temp_id = 'RECIPE_{}'.format(temp_split_line[1])
            recipe_json[temp_id]['source'] = temp_split_line[-1]

        if temp_split_line[0] == 'preptime':
            temp_id = 'RECIPE_{}'.format(temp_split_line[1])
            recipe_json[temp_id]['preptime'] = temp_split_line[-1]

        if temp_split_line[0] == 'cooktime':
            temp_id = 'RECIPE_{}'.format(temp_split_line[1])
            recipe_json[temp_id]['cooktime'] = temp_split_line[-1]

        if temp_split_line[0] == 'waittime':
            temp_id = 'RECIPE_{}'.format(temp_split_line[1])
            recipe_json[temp_id]['waittime'] = temp_split_line[-1]

        if temp_split_line[0] == 'calories':
            temp_id = 'RECIPE_{}'.format(temp_split_line[1])
            recipe_json[temp_id]['calories'] = temp_split_line[-1]

        if temp_split_line[0] == 'carbs':
            temp_id = 'RECIPE_{}'.format(temp_split_line[1])
            recipe_json[temp_id]['carbs'] = temp_split_line[-1]

        if temp_split_line[0] == 'servings':
            temp_id = 'RECIPE_{}'.format(temp_split_line[1])
            recipe_json[temp_id]['servings'] = temp_split_line[-1]

        if temp_split_line[0] == 'protein':
            temp_id = 'RECIPE_{}'.format(temp_split_line[1])
            recipe_json[temp_id]['protein'] = temp_split_line[-1]

        if temp_split_line[0] == 'satfat':
            temp_id = 'RECIPE_{}'.format(temp_split_line[1])
            recipe_json[temp_id]['satfat'] = temp_split_line[-1]

        if temp_split_line[0] == 'sugar':
            temp_id = 'RECIPE_{}'.format(temp_split_line[1])
            recipe_json[temp_id]['sugar'] = temp_split_line[-1]

        if temp_split_line[0] == 'fat':
            temp_id = 'RECIPE_{}'.format(temp_split_line[1])
            recipe_json[temp_id]['fat'] = temp_split_line[-1]

        if temp_split_line[0] == 'fiber':
            temp_id = 'RECIPE_{}'.format(temp_split_line[1])
            recipe_json[temp_id]['fiber'] = temp_split_line[-1]

        if 'ingredients' in temp_split_line[0]:
            ingredients_list.append(temp_split_line[-1].strip('"'))

        if 'instructions' in temp_split_line[0]:
            while 'tags.' not in temp_line:
                if temp_line:
                    if 'instructions,' in temp_line:
                        instructions_list.append(temp_line.split(",")[-1].strip('"'))
                    else:
                        instructions_list.append(temp_line.strip('"'))
                itr += 1
                temp_line = file_lines[itr].strip()

            itr -= 1

        if 'tags.' in temp_split_line[0]:
            tags_list.append(temp_split_line[-1].strip('"'))

    itr += 1


last_tag = temp_id.split("_")[-1]
temp_id_ingredients = 'RECIPE_{}'.format(last_tag)
recipe_json[temp_id_ingredients]['ingredients'] = ingredients_list
recipe_json[temp_id_ingredients]['instructions'] = instructions_list
recipe_json[temp_id_ingredients]['tags'] = tags_list

### NEED TO UPDATE LOCATION OF FILE###
with open('C:/Users/mgruz/Desktop/w210/data/recipe/recipe_all.json', 'w') as fp:
    json.dump(recipe_json, fp)