import pandas as pd
pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
from rootseller import profile
from rootseller import micronutrients
from rootseller import macronutrients


class Nutrition(object):
    def __init__(self):
        try:
            self.nutritional_database = pd.read_csv('C:/Users/mgruz/Desktop/w210/data/nutrient/compiled/nutrition_master_df.csv').fillna(0.0)
        except:
            self.nutritional_database = pd.read_csv('C:/Users/pa351d/Desktop/w210/data/nutrient/compiled/nutrition_master_df.csv').fillna(0.0)


    def NDB_NO_lookup(self, tag, **kwargs):

        if "filter_list" in kwargs.keys():
            return self.nutritional_database[self.nutritional_database['NDB_NO'] == "\"{}\"".format(tag.strip('"'))][kwargs["filter_list"]]
        else:
            return self.nutritional_database[self.nutritional_database['NDB_NO'] ==  "\"{}\"".format(tag.strip('"'))]




init_nutrition = Nutrition().nutritional_database

str_columns = ["Category", "Description", "NDB_NO"]
num_columns = ["10:0 (g)", "12:0 (g)", "13:0 (g)", "14:0 (g)", "14:1 (g)", "15:0 (g)", "15:1 (g)",
                         "16:0 (g)", "16:1 c (g)", "16:1 t (g)", "16:1 undifferentiated (g)", "17:0 (g)",
                         "17:1 (g)", "18:0 (g)", "18:1 c (g)", "18:1 t (g)", "18:1 undifferentiated (g)",
                         "18:1-11 t (18:1t n-7) (g)", "18:2 CLAs (g)", "18:2 i (g)", "18:2 n-6 c,c (g)",
                         "18:2 t not further defined (g)", "18:2 t,t (g)", "18:2 undifferentiated (g)",
                         "18:3 n-3 c,c,c (ALA) (g)", "18:3 n-6 c,c,c (g)", "18:3 undifferentiated (g)", "18:3i (g)",
                         "18:4 (g)", "20:0 (g)", "20:1 (g)", "20:2 n-6 c,c (g)", "20:3 n-3 (g)", "20:3 n-6 (g)",
                         "20:3 undifferentiated (g)", "20:4 n-6 (g)", "20:4 undifferentiated (g)",
                         "20:5 n-3 (EPA) (g)", "21:5 (g)", "22:0 (g)", "22:1 c (g)", "22:1 t (g)",
                         "22:1 undifferentiated (g)", "22:4 (g)", "22:5 n-3 (DPA) (g)", "22:6 n-3 (DHA) (g)",
                         "24:0 (g)", "24:1 c (g)", "4:0 (g)", "6:0 (g)", "8:0 (g)", "Alanine (g)",
                         "Alcohol, ethyl (g)", "Arginine (g)", "Ash (g)", "Aspartic acid (g)", "Beta-sitosterol (mg)",
                         "Betaine (mg)", "Caffeine (mg)", "Calcium, Ca (mg)", "Campesterol (mg)",
                         "Carbohydrate, by difference (g)", "Carotene, alpha (microg)", "Carotene, beta (microg)",
                         "Cholesterol (mg)", "Choline, total (mg)", "Copper, Cu (mg)", "Cryptoxanthin, beta (microg)",
                         "Cystine (g)", "Dihydrophylloquinone (microg)", "Energy (kJ)", "Energy (kcal)",
                         "Fatty acids, total monounsaturated (g)", "Fatty acids, total polyunsaturated (g)",
                         "Fatty acids, total saturated (g)", "Fatty acids, total trans (g)",
                         "Fatty acids, total trans-monoenoic (g)", "Fatty acids, total trans-polyenoic (g)",
                         "Fiber, total dietary (g)", "Fluoride, F (microg)", "Folate, DFE (microg)",
                         "Folate, food (microg)", "Folate, total (microg)", "Folic acid (microg)", "Fructose (g)",
                         "Galactose (g)", "Glucose (dextrose) (g)", "Glutamic acid (g)", "Glycine (g)",
                         "Histidine (g)", "Hydroxyproline (g)", "Iron, Fe (mg)", "Isoleucine (g)", "Lactose (g)",
                         "Leucine (g)", "Lutein + zeaxanthin (microg)", "Lycopene (microg)", "Lysine (g)",
                         "Magnesium, Mg (mg)", "Maltose (g)", "Manganese, Mn (mg)", "Menaquinone-4 (microg)",
                         "Methionine (g)", "Niacin (mg)", "Pantothenic acid (mg)", "Phenylalanine (g)",
                         "Phosphorus, P (mg)", "Phytosterols (mg)", "Potassium, K (mg)", "Proline (g)",
                         "Protein (g)", "Retinol (microg)", "Riboflavin (mg)", "Selenium, Se (microg)",
                         "Sodium, Na (mg)", "Starch (g)", "Stigmasterol (mg)", "Sucrose (g)",
                         "Sugars, total (g)", "Theobromine (mg)", "Thiamin (mg)", "Threonine (g)",
                         "Tocopherol, beta (mg)", "Tocopherol, delta (mg)", "Tocopherol, gamma (mg)",
                         "Tocotrienol, alpha (mg)", "Tocotrienol, beta (mg)", "Tocotrienol, delta (mg)",
                         "Tocotrienol, gamma (mg)", "Total lipid (fat) (g)", "Tryptophan (g)", "Tyrosine (g)",
                         "Valine (g)", "Vitamin A, IU (IU)", "Vitamin A, RAE (microg)", "Vitamin B-12 (microg)",
                         "Vitamin B-12, added (microg)", "Vitamin B-6 (mg)", "Vitamin C, total ascorbic acid (mg)",
                         "Vitamin D (D2 + D3) (microg)", "Vitamin D (IU)", "Vitamin D2 (ergocalciferol) (microg)",
                         "Vitamin D3 (cholecalciferol) (microg)", "Vitamin E (alpha-tocopherol) (mg)",
                         "Vitamin E, added (mg)", "Vitamin K (phylloquinone) (microg)", "Water (g)",
                         "Weight(g)", "Zinc, Zn (mg)", "Serine (g)"]
str_df = init_nutrition[str_columns]
num_df = init_nutrition[num_columns]


itr = 0
while itr < len(init_nutrition):
    conversion_factor = 100.0 / init_nutrition.loc[itr, 'Weight(g)']
    init_nutrition.loc[itr, num_columns] =  num_df.loc[itr, num_columns] * conversion_factor
    num_df.loc[itr, :] = num_df.loc[itr, :] * conversion_factor
    print itr, len(init_nutrition)
    itr += 1

master_df = num_df.join(str_df)
master_df.to_csv('C:/Users/mgruz/Desktop/w210/data/nutrient/compiled/nutrition_master_normalized_df.csv')