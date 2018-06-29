from django.shortcuts import render

def index(request):
    return render(request, 'main_page/index.html')

def about_the_project(request):
    return render(request, 'main_page/about_the_project.html')

def sample_dashboard(request):
    return render(request, 'main_page/sample_dashboard.html')

def recipe_examples(request):
    return render(request, 'main_page/recipe_examples.html')

def survey_example(request):
    return render(request, 'main_page/survey_example.html')

def user_login(request):
    return render(request, 'user_example/templates/registration/login.html')

def user_signup(request):
    return render(request, 'user_example/templates/registration/register.html')
