from django.urls import path, include
from django.contrib import admin

from . import views
# from user_example import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about_the_project/', views.about_the_project, name='about_the_project'),
    path('sample_dashboard/', views.sample_dashboard, name='sample_dashboard'),
    path('recipe_examples/', views.recipe_examples, name='recipe_examples'),
    path('survey_example/', views.survey_example, name='survey_example'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_signup/', views.user_signup, name='user_signup'),

]
