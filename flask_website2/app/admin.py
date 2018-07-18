from django.contrib import admin
from accounts.models import UserProfile, UserPreferences

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserPreferences)
