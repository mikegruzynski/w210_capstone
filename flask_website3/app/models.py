from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from wtforms import Form, FloatField, StringField, SelectField, RadioField #, validators,

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

def __repr__(self):
        return '<User {}>'.format(self.username)

# Model
# TODO: Valdate ranges in filed (optional)
class InputMacroNutrientsForm(Form):
    calories = FloatField()
    protein = FloatField()
    fat = FloatField()
    carbohydrate = FloatField()
    fiber = FloatField()
    cholesterol = FloatField()
    saturated_fat = FloatField()
    unsaturated_fat = FloatField()
    sugar = FloatField()

class InputMicroNutrientsForm(Form):
    Betaine = FloatField()
    Calcium = FloatField()
    Choline = FloatField()
    Copper = FloatField()
    Fluoride = FloatField()
    Folate = FloatField()
    Folate_DFE = FloatField()
    Folate_food = FloatField()
    Folic_acid = FloatField()
    Iron = FloatField()
    Magnesium = FloatField()
    Manganese = FloatField()
    Niacin = FloatField()
    Fluoride = FloatField()
    Pantothenic_acid = FloatField()
    Phosphorus = FloatField()
    Potassium = FloatField()
    Retinol = FloatField()
    Riboflavin = FloatField()
    Selenium = FloatField()
    Sodium = FloatField()
    Fluoride = FloatField()
    Thiamin = FloatField()
    Vitamin_A = FloatField()
    Vitamin_B12 = FloatField()
    Vitamin_B12_added = FloatField()
    Vitamin_B6 = FloatField()
    Vitamin_C = FloatField()
    Vitamin_D = FloatField()
    Vitamin_D2 = FloatField()
    Vitamin_D3 = FloatField()
    Vitamin_E = FloatField()
    Vitamin_E_added = FloatField()
    Vitamin_K = FloatField()
    Zinc = FloatField()

class ChooseRecipeToSubIngredients(Form):
    recipe_name = StringField()

class IgnoreRecipeForm(Form):
    ignore_list = StringField()

class IngredientSubForm(Form):
    ingredientSub = StringField()
    # foodType = StringField()
    foodType = SelectField('type', choices=[('1','Baked'), ('2','Beef'),
    ('3','Beverages'), ('4','Breakfast_Cereals'), ('5','Cereal_Grains_and_Pasta'),
    ('6','Dairy_and_Egg'), ('7','Fats_and_Oils'), ('8','Finfish_and_Shellfish'),
    ('9','Fruits_and_Fruit_Juices'), ('10','Lamb_Veal_and_Game'), ('11','Legumes_and_Legume'),
    ('12','Nut_and_Seed'), ('13','Pork'), ('14','Poultry'), ('15','Sausages_and_Luncheon_Meats'),
    ('16','Soups_Sauces_and_Gravies'), ('17','Spices_and_Herbs'),
    ('18','Sweets'), ('19','Vegetables_and_Vegetable')])
    # replacemnetChoice = StringField()
    replacementChoice = RadioField('', choices=[('1', '1'), ('2','2'), ('3','3'), ('DNR', 'Do Not Replace')])

class UserPreference(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    firstname = db.Column(db.String(64), index=True, unique=True)
    lastname = db.Column(db.String(64), index=True, unique=True)
    gender = db.Column(db.String(64), index=True, unique=True)
    age = db.Column(db.Integer, index=True)
    weight_lb = db.Column(db.Integer, index=True)
    height_in = db.Column(db.Integer, index=True)
    foods_allergic = db.Column(db.String(1200), index=True)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
