import pandas as pd
import csv
import os
from nutrient_db.models import Nutritional_database

# macro_list = ['Energy (kcal)', 'Total lipid (fat) (g)', 'Carbohydrate, by difference (g)',
# 'Fiber, total dietary (g)', 'Cholesterol (mg)',
# 'Fatty acids, total saturated (g)',
# 'Fatty acids, total monounsaturated (g)', 'Fatty acids, total polyunsaturated (g)',
#  'Fatty acids, total trans (g)' ]
#
# # path = '/root/w210_capstone/data/nutrient/compiled'
# path = '/Users/mauracullen/Documents/UCB_MIDS/W210_Capstone/w210_capstone/data/nutrient/compiled'
# nutritional_database = pd.read_csv(path+'/nutrition_master_df.csv')
#
# micro_list = ['Iron, Fe (mg)', 'Magnesium, Mg (mg)', 'Manganese, Mn (mg)', 'Thiamin (mg)',
#  'Vitamin D (D2 + D3) (µg)']
#
# keep_list = ['NDB_NO', 'Measure', 'Weight(g)', 'Description', 'Category']
#
# macro_micro_list = keep_list + macro_list + micro_list
# ndb_columns_filtered = nutritional_database[macro_micro_list]
# ndb_columns_filtered['NDB_NO'] = ndb_columns_filtered['NDB_NO'].str.strip('"')
# ndb_columns_filtered.to_csv(path+'ndb_columns_filtered2.csv')

path = '/Users/mauracullen/Documents/UCB_MIDS/W210_Capstone/w210_capstone/data/nutrient/compiled'
with open(path+'ndb_columns_filtered2.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for i, row in enumerate(reader):
        p = Nutritional_database(NDB_NO=row['NDB_NO'], Measure=row['Measure'],
                                 Weight_g = row['Weight_g'], Description = row['Description'],
                                 Category = row['Category'], Energy_kcal = row['Energy_kcal'],
                                 Total_lipid_fat_g = row['Total_lipid_fat_g'],
                                 Carbohydrate_by_diff_g = row['Carbohydrate_by_diff_g'],
                                 Fiber_total_dietary_g = row['Fiber_total_dietary_g'],
                                 Cholesterol_mg = row['Cholesterol_mg'],
                                 Fatty_acids_saturated_g = row['Fatty_acids_saturated_g'],
                                 Fatty_acids_total_monounsaturated_g = row['Fatty_acids_total_monounsaturated_g'],
                                 Fatty_acids_total_polyunsaturated_g = row['Fatty_acids_total_polyunsaturated_g'],
                                 Fatty_acids_total_trans_g = row['Fatty_acids_total_trans_g'],
                                 Iron_mg = row['Iron_mg'], Magnesium_mg = row['Magnesium_mg'],
                                 Magnesium_mng = row['Magnesium_mng'],
                                 Thiamin_mg = row['Thiamin_mg'], Vitamin_D_microg = row['Vitamin_D_microg']
                                 )
        p.save()
