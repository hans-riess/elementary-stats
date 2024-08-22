from django import forms
from .models import Response
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['answer']
    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

class ResultsForm(forms.ModelForm):
    pass

class BinsForm(forms.Form):
    bins = forms.IntegerField(label='Number of Bins', min_value=1, initial=10)