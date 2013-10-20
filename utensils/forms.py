# encoding: utf-8
from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(
        label='', required=False,
        widget=forms.widgets.TextInput())
