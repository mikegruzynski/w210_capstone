from pandas import *
set_option('display.height', 1000)
set_option('display.max_rows', 500)
set_option('display.max_columns', 500)
set_option('display.width', 1000)

nutrition_info_food_group_dict = {'American Indian/Alaska Native Foods': 24,
                                  'Baby Foods': 3,
                                  'Baked Products': 18,
                                  'Beef Products': 13,
                                  'Beverages': 14,
                                  'Breakfast Cereals': 8,
                                  'Cereal Grains and Pasta': 24,
                                  'Dairy and Egg Products': 1,
                                  'Fast Foods': 21,
                                  'Fats and Oils': 4,
                                  'Finfish and Shellfish Products': 15,
                                  'Fruits and Fruit Juices': 24,
                                  'Lamb, Veal, and Game Products': 17,
                                  'Legumes and Legume Products': 16,
                                  'Meals, Entrees, and Side Dishes': 22,
                                  'Nut and Seed Products': 12,
                                  'Pork Products': 10,
                                  'Poultry Products': 5,
                                  'Restaurant Foods': 25,
                                  'Sausages and Luncheon Meats': 7,
                                  'Snacks': 23,
                                  'Soups, Sauces, and Gravies': 6,
                                  'Spices and Herbs': 2,
                                  'Sweets': 19,
                                  'Vegetables and Vegetable Products': 11}

### CHANGE DIRECTORY ###
raw_dir = 'C:/Users/mgruz/Desktop/w210/data/nutrient/raw/'
### CHANGE DIRECTORY ###

for food in nutrition_info_food_group_dict.keys():
    print food
    food = food.replace(" ", "_").replace("/", "_")
    ### CHANGE DIRECTORY ###
    raw_dir = 'C:/Users/mgruz/Desktop/w210/data/nutrient/raw/'
    ### CHANGE DIRECTORY ###
    master_df_list = []
    for i in range(50):
        temp_file = raw_dir + '{}_{}.csv'.format(food, i)
        header_use = ['NDB_NO', 'Description', 'Weight(g)', 'Measure']
        try:
            df_temp = read_csv(temp_file, header=None, skiprows=[0, 1, 2, 3, 4, 5, 6, 7])
            df_temp = df_temp.loc[:, :3]
            df_temp.columns = header_use
            master_df_list.append(df_temp)
        except:
            print "\tPASS", food, i

    master_df = concat(master_df_list)
    master_df = master_df.drop_duplicates(subset='NDB_NO')

    for i in range(50):
        temp_file = raw_dir + '{}_{}.csv'.format(food, i)
        with open(temp_file) as f:
            lines = f.readlines()
            header = lines[1]
            header = header.replace('"', '').replace('Per Measure', '').strip("\n").split("Nutrients:")[-1].split(';')
            header = [x.lstrip(' ') for x in header]
            header_use = ['NDB_NO', 'Description', 'Weight(g)', 'Measure'] + header

        try:
            df_temp = read_csv(temp_file, header=None, skiprows=[0, 1, 2, 3, 4, 5, 6, 7])
            df_temp = df_temp.loc[:, :6]
            df_temp.columns = header_use
            df_temp = df_temp[['NDB_NO'] + header]
        except:
            try:
                df_temp = read_csv(temp_file, header=None, skiprows=[0, 1, 2, 3, 4, 5, 6, 7])
                df_temp = df_temp.loc[:, :5]
                df_temp.columns = header_use
                df_temp = df_temp[['NDB_NO'] + header]
            except:
                print "\tPASS", food, i

        if i == 0:
            master_df_use = merge(master_df, df_temp, how='left', on=['NDB_NO'])
        else:
            master_df_use = merge(master_df_use, df_temp, how='left', on=['NDB_NO'])

    master_df_use = master_df_use.replace('--', np.NaN)

    ### CHANGE DIRECTORY ###
    master_df_use.to_csv('C:/Users/mgruz/Desktop/w210/data/nutrient/compiled/{}_master_df.csv'.format(food))
    ### CHANGE DIRECTORY ###

    print "\n"
    print "\n"
    print "\n"
    print "\tFood:", food, " FINISHED PARSE"
    print "\t", master_df_use.shape
    print "\n"
    print "\n"
    print "\n"