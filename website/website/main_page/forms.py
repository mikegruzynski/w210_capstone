from django import forms

class PrefForm(forms.Form):
    post = forms.CharField()
