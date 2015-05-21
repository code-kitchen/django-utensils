from django import forms

from utensils.forms import UniqueModelFieldsMixin

from .models import Book


class BookForm(UniqueModelFieldsMixin, forms.ModelForm):
    unique_fields = [{'field': 'title', 'case_insensitive': True}]

    class Meta:
        model = Book
        fields = ('author', 'title', 'publication_date', 'in_stock')
