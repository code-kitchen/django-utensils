from utensils.views import BaseListView, SetModelFieldView

from .models import Author, Book


class BookListView(BaseListView):
    model = Book
    # Used by SearchFormMixin:
    search_fields = {
        'title':                'icontains',
        'author__first_name':   'icontains',
        'author__middle_names': 'icontains',
        'author__last_name':    'icontains',
    }


class SetNotInStockView(SetModelFieldView):
    model = Book
    field = 'in_stock'
    value = False
    template_name = 'example/book_confirm_out_of_stock.html'
