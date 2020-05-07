from django import forms
from . import models

attrs = {
    'id': 'textarea',
    'autocomplete': 'on',
    'cols': '',
    'rows': ''
}


class CreateTwit(forms.ModelForm):
    attrs['placeholder'] = 'Что происходит?'
    content = forms.CharField(widget=forms.Textarea(attrs=attrs), label='', required=True, max_length=235)

    class Meta:
        model = models.Twit
        fields = ['content']


class SearchForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs=attrs), label='', required=True, max_length=235)

    class Meta:
        model = models.Twit
        fields = ['content']