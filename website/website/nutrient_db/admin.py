from django.contrib import admin

from .models import Nutritional_database
from .models import Substitution_list

admin.site.register(Nutritional_database)
admin.site.register(Substitution_list)
admin.site.siteheader = 'Root Cellar Administer'
