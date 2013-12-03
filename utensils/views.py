# encoding: utf-8
from django.views.generic import ListView
from django.views.generic.detail import (
    BaseDetailView, SingleObjectTemplateResponseMixin)

from .viewmixins import (
    OrderByMixin, PaginateMixin, SearchFormMixin, SetModelFieldMixin)


class BaseListView(PaginateMixin, OrderByMixin, SearchFormMixin, ListView):
    """
    Defines a base list view that supports pagination, ordering and basic search.
    
    Supports a filter description that can be used in templates:
    
        class ActiveCustomerList(BaseListView):
            filter_description = u"Active"
            queryset = Customer.active.all()
    
    
        {% block content %}
          <h2>
            {% if filter_description %}
              {{ filter_description|title }} customers
            {% else %}
              Customers
            {% endif %}
          </h2>
          <! -- more template -->
        {% end block %}
    """
    def get_filter_description(self):
        if hasattr(self, 'filter_description'):
            return self.filter_description
    
    def get_context_data(self, **kwargs):
        data = super(BaseListView, self).get_context_data(**kwargs)
        filter_description = self.get_filter_description()
        if filter_description:
            data.update({'filter_description': filter_description})
        return data


class BaseSetModelFieldView(SetModelFieldMixin, BaseDetailView):
    """
    Base view for setting a single value on a model instance.

    Using this base class requires subclassing to provide a response mixin.
    """


class SetModelFieldView(BaseSetModelFieldView,
        SingleObjectTemplateResponseMixin):
    """
    View for setting a single value on an object on POST. GET should be used for
    a confirmation view.

    Required class settings:
        * `field` or `get_field()` - string containing the field name to alter
        * `value` or `get_value()` - the value to set the field to
    """
