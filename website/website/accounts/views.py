from django.shortcuts import render
from accounts.forms import RegistraionForm

# accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView

class SignUp(generic.CreateView):
    # form_class = UserCreationForm
    form_class = RegistraionForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
