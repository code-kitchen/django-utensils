# encoding: utf-8
from django import forms
from django.utils.functional import curry


class SearchForm(forms.Form):
    """
    Generic search form that can be used on any page.
    
    Used by viewmixins.SearchFormMixin.
    """
    search = forms.CharField(
        label='', required=False,
        widget=forms.widgets.TextInput())


class UniqueModelFieldsMixin(object):
    """
    Mixin that enforces unique fields on ModelForm forms to negate the need to
    redefine fields that are required where blank=True on the model field.

    Must be left of ModelForm when defining the form class (see
    https://code.djangoproject.com/ticket/13075).

    unique_fields = ['name', 'username']
    unique_fields = ['name',  {'field': 'username', 'case_insensitive': True}]
    """
    unique_fields = []

    def __init__(self, *args, **kwargs):
        super(UniqueModelFieldsMixin, self).__init__(*args, **kwargs)

        def _make_validator(field, case_insensitive):
            model = self.Meta.model
            value = self.cleaned_data.get(field)

            case = 'i' if case_insensitive else ''
            qs = model.objects.filter(
                **{field + '__{}exact'.format(case): value})
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError(
                    "That {} is not available.".format(field.replace('_', ' ')))
            return value

        for field in self.unique_fields:
            if isinstance(field, dict):
                case_insensitive = field.get('case_insensitive', False)
                field_name = field['field']
            else:
                field_name = field
                case_insensitive = False
            func_name = "clean_{}".format(field_name)
            setattr(self, func_name,
                curry(_make_validator, field_name, case_insensitive))
