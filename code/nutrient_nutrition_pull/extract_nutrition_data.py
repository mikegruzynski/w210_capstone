import requests
from bs4 import BeautifulSoup
import urllib
import os

nutrition_url = 'https://ndb.nal.usda.gov/ndb/nutrients/report/nutrientsfrm?max=25&offset=0&totCount=0&nutrient1=255&nutrient2=208&nutrient3=268&fg=11&subset=0&sort=f&measureby=m'

nutrition_info_food_group_dict = {'American Indian/Alaska Native Foods': 24,
                                  'Baby Foods': 3,
                                  'Baked Products': 18,
                                  'Beef Products': 13,
                                  'Beverages': 14,
                                  'Breakfast Cereals': 8,
                                  'Cereal Grains and Pasta': 20,
                                  'Dairy and Egg Products': 1,
                                  'Fast Foods': 21,
                                  'Fats and Oils': 4,
                                  'Finfish and Shellfish Products': 15,
                                  'Fruits and Fruit Juices': 9,
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

nutrition_info_nutrient_dict = {"Water (g)": 255,
                                "Energy (kcal)": 208,
                                "Energy (kJ)": 268,
                                "Protein (g)": 203,
                                "Total lipid (fat) (g)": 204,
                                "Ash (g)": 207,
                                "Carbohydrate, by difference (g)": 205,
                                "Fiber, total dietary (g)": 291,
                                "Sugars, total (g)": 269,
                                "Sugars, added (g)": 539,
                                "Sucrose (g)": 210,
                                "Glucose (dextrose) (g)": 211,
                                "Fructose (g)": 212,
                                "Lactose (g)": 213,
                                "Maltose (g)": 214,
                                "Galactose (g)": 287,
                                "Starch (g)": 209,
                                "Calcium, Ca (mg)": 301,
                                "Iron, Fe (mg)": 303,
                                "Magnesium, Mg (mg)": 304,
                                "Phosphorus, P (mg)": 305,
                                "Potassium, K (mg)": 306,
                                "Sodium, Na (mg)": 307,
                                "Zinc, Zn (mg)": 309,
                                "Copper, Cu (mg)": 312,
                                "Manganese, Mn (mg)": 315,
                                "Selenium, Se (mcg)": 317,
                                "Fluoride, F (mcg)": 313,
                                "Vitamin C, total ascorbic acid (mg)": 401,
                                "Thiamin (mg)": 404,
                                "Riboflavin (mg)": 405,
                                "Niacin (mg)": 406,
                                "Pantothenic acid (mg)": 410,
                                "Vitamin B-6 (mg)": 415,
                                "Folate, total (mcg)": 417,
                                "Folic acid (mcg)": 431,
                                "Folate, food (mcg)": 432,
                                "Folate, DFE (mcg)": 435,
                                "Choline, total (mg)": 421,
                                "Betaine (mg)": 454,
                                "Vitamin B-12 (mcg)": 418,
                                "Vitamin B-12, added (mcg)": 578,
                                "Vitamin A, RAE (mcg)": 320,
                                "Retinol (mcg)": 319,
                                "Carotene, beta (mcg)": 321,
                                "Carotene, alpha (mcg)": 322,
                                "Cryptoxanthin, beta (mcg)": 334,
                                "Vitamin A, IU (IU)": 318,
                                "Lycopene (mcg)": 337,
                                "Lutein + zeaxanthin (mcg)": 338,
                                "Vitamin E (alpha-tocopherol) (mg)": 323,
                                "Vitamin E, added (mg)": 573,
                                "Tocopherol, beta (mg)": 341,
                                "Tocopherol, gamma (mg)": 342,
                                "Tocopherol, delta (mg)": 343,
                                "Tocotrienol, alpha (mg)": 344,
                                "Tocotrienol, beta (mg)": 345,
                                "Tocotrienol, gamma (mg)": 346,
                                "Tocotrienol, delta (mg)": 347,
                                "Vitamin D (D2 + D3) (mcg)": 328,
                                "Vitamin D2 (ergocalciferol) (mcg)": 325,
                                "Vitamin D3 (cholecalciferol) (mcg)": 326,
                                "Vitamin D (IU)": 324,
                                "Vitamin K (phylloquinone) (mcg)": 430,
                                "Dihydrophylloquinone (mcg)": 429,
                                "Menaquinone-4 (mcg)": 428,
                                "Fatty acids, total saturated (g)": 606,
                                "4:0 (g)": 607,
                                "6:0 (g)": 608,
                                "8:0 (g)": 609,
                                "10:0 (g)": 610,
                                "12:0 (g)": 611,
                                "13:0 (g)": 696,
                                "14:0 (g)": 612,
                                "15:0 (g)": 652,
                                "16:0 (g)": 613,
                                "17:0 (g)": 653,
                                "18:0 (g)": 614,
                                "20:0 (g)": 615,
                                "22:0 (g)": 624,
                                "24:0 (g)": 654,
                                "Fatty acids, total monounsaturated (g)": 645,
                                "14:1 (g)": 625,
                                "15:1 (g)": 697,
                                "16:1 undifferentiated (g)": 626,
                                "16:1 c (g)": 673,
                                "16:1 t (g)": 662,
                                "17:1 (g)": 687,
                                "18:1 undifferentiated (g)": 617,
                                "18:1 c (g)": 674,
                                "18:1 t (g)": 663,
                                "18:1-11 t (18:1t n-7) (g)": 859,
                                "20:1 (g)": 628,
                                "22:1 undifferentiated (g)": 630,
                                "22:1 c (g)": 676,
                                "22:1 t (g)": 664,
                                "24:1 c (g)": 671,
                                "Fatty acids, total polyunsaturated (g)": 646,
                                "18:2 undifferentiated (g)": 618,
                                "18:2 n-6 c,c (g)": 675,
                                "18:2 CLAs (g)": 670,
                                "18:2 t,t (g)": 669,
                                "18:2 i (g)": 666,
                                "18:2 t not further defined (g)": 665,
                                "18:3 undifferentiated (g)": 619,
                                "18:3 n-3 c,c,c (ALA) (g)": 851,
                                "18:3 n-6 c,c,c (g)": 685,
                                "18:3i (g)": 856,
                                "18:4 (g)": 627,
                                "20:2 n-6 c,c (g)": 672,
                                "20:3 undifferentiated (g)": 689,
                                "20:3 n-3 (g)": 852,
                                "20:3 n-6 (g)": 853,
                                "20:4 undifferentiated (g)": 620,
                                "20:4 n-6 (g)": 855,
                                "20:5 n-3 (EPA) (g)": 629,
                                "21:5 (g)": 857,
                                "22:4 (g)": 858,
                                "22:5 n-3 (DPA) (g)": 631,
                                "22:6 n-3 (DHA) (g)": 621,
                                "Fatty acids, total trans (g)": 605,
                                "Fatty acids, total trans-monoenoic (g)": 693,
                                "Fatty acids, total trans-polyenoic (g)": 695,
                                "Cholesterol (mg)": 601,
                                "Phytosterols (mg)": 636,
                                "Stigmasterol (mg)": 638,
                                "Campesterol (mg)": 639,
                                "Beta-sitosterol (mg)": 641,
                                "Tryptophan (g)": 501,
                                "Threonine (g)": 502,
                                "Isoleucine (g)": 503,
                                "Leucine (g)": 504,
                                "Lysine (g)": 505,
                                "Methionine (g)": 506,
                                "Cystine (g)": 507,
                                "Phenylalanine (g)": 508,
                                "Tyrosine (g)": 509,
                                "Valine (g)": 510,
                                "Arginine (g)": 511,
                                "Histidine (g)": 512,
                                "Alanine (g)": 513,
                                "Aspartic acid (g)": 514,
                                "Glutamic acid (g)": 515,
                                "Glycine (g)": 516,
                                "Proline (g)": 517,
                                "Serine (g)": 518,
                                "Hydroxyproline (g)": 521,
                                "Alcohol, ethyl (g)": 221,
                                "Caffeine (mg)": 262,
                                "Theobromine (mg)": 263}

for food in nutrition_info_food_group_dict:
    print food
    itr = 0
    itr_2 = 0
    while itr < len(nutrition_info_nutrient_dict.keys()):
        if itr_2 == 49:
            initial_website = 'https://ndb.nal.usda.gov/ndb/nutrients/report/nutrientsfrm?max=25&offset=0&totCount=0&nutrient1={}&nutrient2={}&nutrient3=&fg={}&subset=0&sort=f&measureby=m'.format(
                nutrition_info_nutrient_dict[nutrition_info_nutrient_dict.keys()[itr]],
                nutrition_info_nutrient_dict[nutrition_info_nutrient_dict.keys()[itr + 1]],
                nutrition_info_food_group_dict[food])
        else:
            initial_website = 'https://ndb.nal.usda.gov/ndb/nutrients/report/nutrientsfrm?max=25&offset=0&totCount=0&nutrient1={}&nutrient2={}&nutrient3={}&fg={}&subset=0&sort=f&measureby=m'.format(
                nutrition_info_nutrient_dict[nutrition_info_nutrient_dict.keys()[itr]],
                nutrition_info_nutrient_dict[nutrition_info_nutrient_dict.keys()[itr + 1]],
                nutrition_info_nutrient_dict[nutrition_info_nutrient_dict.keys()[itr + 2]],
                nutrition_info_food_group_dict[food])
        # driver.get(initial_website)

        amount_of_food = 10000
        soup = BeautifulSoup(requests.get(initial_website).text, "lxml")
        for item in soup.findAll("div", class_="alert alert-info result-message"):
            for line in item.text.split("\n"):
                if 'foods found for this report' in line:
                    amount_of_food = int(line.strip().split(" ")[0])

        if itr_2 == 49:
            download_website = 'https://ndb.nal.usda.gov/ndb/nutrients/download?nutrient1={}&nutrient2={}&nutrient3=&fg={}&subset=0&sort=f&totCount={}&max=&measureby=m'.format(
                nutrition_info_nutrient_dict[nutrition_info_nutrient_dict.keys()[itr]],
                nutrition_info_nutrient_dict[nutrition_info_nutrient_dict.keys()[itr + 1]],
                nutrition_info_food_group_dict[food],
                amount_of_food)
        else:
            download_website = 'https://ndb.nal.usda.gov/ndb/nutrients/download?nutrient1={}&nutrient2={}&nutrient3={}&fg={}&subset=0&sort=f&totCount={}&max=&measureby=m'.format(
                nutrition_info_nutrient_dict[nutrition_info_nutrient_dict.keys()[itr]],
                nutrition_info_nutrient_dict[nutrition_info_nutrient_dict.keys()[itr + 1]],
                nutrition_info_nutrient_dict[nutrition_info_nutrient_dict.keys()[itr + 2]],
                nutrition_info_food_group_dict[food],
                amount_of_food)

        ### CHANGE DIRECTORY ###
        save_file = 'C:/Users/mgruz/Desktop/w210/data/nutrient/raw/{}_{}.csv'.format(food.replace(" ", "_").replace("/", "_"), itr_2)
        ### CHANGE DIRECTORY ###
        urllib.urlretrieve(download_website, save_file)
        urllib.urlcleanup()
        itr += 3

        print "\t Itr: ", itr_2, " out of 49 complete"

        itr_2 += 1

