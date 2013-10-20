# encoding: utf-8
from django.views.generic import ListView

from .viewmixins import OrderByMixin, PaginateMixin, SearchFormMixin


class BaseListView(PaginateMixin, OrderByMixin, SearchFormMixin, ListView):

    def get_filter_description(self):
        if hasattr(self, 'filter_description'):
            return self.filter_description
    
    def get_context_data(self, **kwargs):
        data = super(BaseListView, self).get_context_data(**kwargs)
        filter_description = self.get_filter_description()
        if filter_description:
            data.update({'filter_description': filter_description})
        return data
