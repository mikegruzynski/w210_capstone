from django.db import models

# Create your models here.
class Substitution_list(models.Model):
    Substitution = models.CharField(max_length=500)
    Ingredient = models.CharField(max_length=500)

    def __str__(self):
        return self.Substitution



class Nutritional_database(models.Model):
    NDB_NO = models.BigIntegerField()
    Measure = models.CharField(max_length=20, default='')
    Weight_g = models.DecimalField(decimal_places = 4, max_digits = 20, default=-1)
    Description = models.CharField(max_length=200, default='')
    Category = models.CharField(max_length=200, default=-1)
    Energy_kcal = models.CharField(max_length=20, default='')
    Total_lipid_fat_g = models.CharField(max_length=20, default='')
    Carbohydrate_by_diff_g = models.CharField(max_length=20, default='')
    Fiber_total_dietary_g = models.CharField(max_length=20, default='')
    Cholesterol_mg = models.CharField(max_length=20, default='')
    Fatty_acids_saturated_g = models.CharField(max_length=20, default='')
    Fatty_acids_total_monounsaturated_g = models.CharField(max_length=20, default='')
    Fatty_acids_total_polyunsaturated_g = models.CharField(max_length=20, default='')
    Fatty_acids_total_trans_g = models.CharField(max_length=20, default='')
    Iron_mg = models.CharField(max_length=20, default='')
    Magnesium_mg = models.CharField(max_length=20, default='')
    Magnesium_mng = models.CharField(max_length=20, default='')
    Thiamin_mg = models.CharField(max_length=20, default='')
    Vitamin_D_microg = models.CharField(max_length=20, default='')

# class Nutritional_database(models.Model):
#     NDB_NO = models.BigIntegerField()
#     Measure = models.CharField(max_length=20, default='')
#     Weight_g = models.DecimalField(decimal_places = 4, max_digits = 20, default=-1)
#     Description = models.CharField(max_length=200, default='')
#     Category = models.CharField(max_length=200, default=-1)
#     Energy_kcal = models.DecimalField(decimal_places = 4, max_digits = 20, default=-1)
#     Total_lipid_fat_g = models.DecimalField(decimal_places = 4, max_digits = 20, default=-1)
#     Carbohydrate_by_diff_g = models.DecimalField(decimal_places = 4, max_digits = 20, default=-1)
#     Fiber_total_dietary_g = models.DecimalField(decimal_places = 4, max_digits = 20, default=-1)
#     Cholesterol_mg = models.DecimalField(decimal_places = 4, max_digits = 20, default=-1)
#     Fatty_acids_saturated_g = models.DecimalField(decimal_places = 4, max_digits = 20, default=-1)
#     Fatty_acids_total_monounsaturated_g = models.DecimalField(decimal_places = 4, max_digits = 20, default=-1)
#     Fatty_acids_total_polyunsaturated_g = models.DecimalField(decimal_places = 4, max_digits = 20, default=-1)
#     Fatty_acids_total_trans_g = models.DecimalField(decimal_places = 4, max_digits = 20, default=-1)
#     Iron_mg = models.DecimalField(decimal_places = 4, max_digits = 20, default=-1)
#     Magnesium_mg = models.DecimalField(decimal_places = 4, max_digits = 20, default=-1)
#     Magnesium_mng = models.DecimalField(decimal_places = 4, max_digits = 20, default=-1)
#     Thiamin_mg = models.DecimalField(decimal_places = 4, max_digits = 20, default=-1)
#     Vitamin_D_microg = models.DecimalField(decimal_places = 4, max_digits = 20, default=-1)

    def __str__(self):
        return self.NDB_NO
