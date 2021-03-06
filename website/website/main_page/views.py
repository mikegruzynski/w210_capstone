from django.shortcuts import render
from django.views.generic import TemplateView
from main_page.forms import PrefForm

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

def user_profile(request):
    return render(request, 'main_page/user_profile.html')

def pref_form(request):
    return render(request, 'main_page/user_preferences.html')
    # template_name = 'main_page/user_preferences.html'
    #
    # def get(self, request):
    #     form = PrefForm()
    #     return render(request, self.template_name, {'form': form})

def home_form(TemplateView):
    template_name='main_page/home_form.html'

    return render(request, self.template_name, {'form':form})
