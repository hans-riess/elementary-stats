from django import forms
from .models import Response

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['answer']

class ResultsForm(forms.ModelForm):
    pass

class BinsForm(forms.Form):
    bins = forms.IntegerField(label='Number of Bins', min_value=1, initial=10)