from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, UpdateView

from utensils.views import BaseListView, SetModelFieldView
from utensils.viewmixins import MessageMixin, PermissionRequiredMixin

from .forms import BookForm
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


class ToggleNotInStockView(SetModelFieldView):
    model = Book
    field = 'in_stock'
    value = False
    template_name = 'example/book_confirm_toggle_stock.html'

    def get_value(self):
        return not self.object.in_stock

    def get_success_url(self):
        return reverse_lazy('book_list')


class BookUpdateView(MessageMixin, UpdateView):
    model = Book
    form_class = BookForm
    permission_required = ''
    success_message = 'Successfully updated the book details!'
    error_message = 'Hmm, could not update the book details.'
    template_name = 'utensils/object_form.html'

    def get_success_url(self):
        return reverse_lazy('book_list')
