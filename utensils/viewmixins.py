# encoding: utf-8
from functools import reduce
import operator
try:
    # Python 3.
    from urllib.parse import urlsplit
except ImportError:
    # Python 2.
    from urllib import urlsplit

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.core.urlresolvers import resolve, Resolver404
from django.db.models import Q
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.http import HttpResponseRedirect

from braces.views import StaffuserRequiredMixin
try:
    from braces.views._access import AccessMixin
except ImportError:
    from braces.views import AccessMixin

from .forms import SearchForm


class MessageMixin(object):
    """
    Make it easy to display notification messages when using Class Based Views.
    """
    def delete(self, request, *args, **kwargs):
        if not self.request.is_ajax() and hasattr(self, 'success_message'):
            messages.success(self.request, self.success_message)
        return super(MessageMixin, self).delete(request, *args, **kwargs)

    def form_valid(self, form):
        if not self.request.is_ajax() and hasattr(self, 'success_message'):
            messages.success(self.request, self.success_message)
        return super(MessageMixin, self).form_valid(form)

    def forms_valid(self, *args, **kwargs):
        if not self.request.is_ajax() and hasattr(self, 'success_message'):
            messages.success(self.request, self.success_message)
        return super(MessageMixin, self).forms_valid(*args, **kwargs)

    def formset_valid(self, form):
        if not self.request.is_ajax() and hasattr(self, 'success_message'):
            messages.success(self.request, self.success_message)
        return super(MessageMixin, self).formset_valid(form)

    def form_invalid(self, form):
        if not self.request.is_ajax() and hasattr(self, 'error_message'):
            messages.error(self.request, self.error_message)
        return super(MessageMixin, self).form_invalid(form)

    def forms_invalid(self, *args, **kwargs):
        if not self.request.is_ajax() and hasattr(self, 'error_message'):
            messages.error(self.request, self.error_message)
        return super(MessageMixin, self).forms_invalid(*args, **kwargs)

    def formset_invalid(self, form):
        if not self.request.is_ajax() and hasattr(self, 'error_message'):
            messages.error(self.request, self.error_message)
        return super(MessageMixin, self).formset_invalid(form)

    def set_value(self, request, *args, **kwargs):
        if not self.request.is_ajax() and hasattr(self, 'success_message'):
            messages.success(self.request, self.success_message)
        return super(MessageMixin, self).set_value(request, *args, **kwargs)


class PermissionRequiredMixin(AccessMixin):
    """
    ** Modified brack3t django-braces mixin to allow a bypass **

    View mixin which verifies that the logged in user has the specified
    permission.

    Class Settings
    `permission_required` - the permission to check for or False to skip check
    `login_url` - the login url of site
    `redirect_field_name` - defaults to "next"
    `raise_exception` - defaults to False - raise 403 if set to True

    Example Usage

        class SomeView(PermissionRequiredMixin, ListView):
            ...
            # required
            permission_required = "app.permission"

            # optional
            login_url = "/signup/"
            redirect_field_name = "hollaback"
            raise_exception = True
            ...
    """
    permission_required = None  # Default required perms to none

    def dispatch(self, request, *args, **kwargs):
        # Make sure that the permission_required attribute is set on the
        # view, or raise a configuration error.
        if self.permission_required is None:
            raise ImproperlyConfigured(
                "'PermissionRequiredMixin' requires "
                "'permission_required' attribute to be set.")

        if self.permission_required is not False:
            # Check to see if the request's user has the required permission.
            has_permission = request.user.has_perm(self.permission_required)

            if not has_permission:  # If the user lacks the permission
                if self.raise_exception:  # *and* if an exception was desired
                    raise PermissionDenied  # return a forbidden response.
                else:
                    return redirect_to_login(request.get_full_path(),
                                             self.get_login_url(),
                                             self.get_redirect_field_name())

        return super(PermissionRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class RedirectToNextMixin(object):
    def post(self, *args, **kwargs):
        next = self.request.GET.get('next')
        if next:
            current_url = self.request.get_full_path()
            redirect_url = current_url.split('next=')[1]
            try:
                split = urlsplit(redirect_url)
                resolve(split.path)
                self.success_url = split.path
            except Resolver404:
                pass
        return super(RedirectToNextMixin, self).post(*args, **kwargs)


class StaffViewMixin(MessageMixin, RedirectToNextMixin, StaffuserRequiredMixin,
                     PermissionRequiredMixin):
    pass


class PaginateMixin(object):
    """
    Adds page size support to a ListView.
    """
    def get_paginate_by(self, *args, **kwargs):
        try:
            paginate_by = self.request.GET['per-page']
            paginate_by = int(paginate_by)
        except (KeyError, ValueError):
            try:
                paginate_by = settings.PAGINATION_PAGE_SIZES[0]
            except (AttributeError, IndexError):
                paginate_by = 20
        return paginate_by


class OrderByMixin(object):
    """
    Add support for ordering the queryset in your ListView.
    """
    def get_queryset(self):
        qs = super(OrderByMixin, self).get_queryset()
        if qs:
            sort_col = self.request.GET.get('sort-col')
            sort_dir = self.request.GET.get('sort-dir', '')
            if sort_col:
                order_by = '%s%s' % ('-' if sort_dir == 'desc' else '', sort_col)
                qs = qs.order_by(order_by)
        return qs

    def get_context_data(self, **kwargs):
        context_data = super(OrderByMixin, self).get_context_data(**kwargs)
        context_data.update({
            'sort-col': self.request.GET.get('sort-col', ''),
            'sort-dir': self.request.GET.get('sort-dir', ''),
        })
        return context_data


class SearchFormMixin(object):
    """
    Present a form element to filter a ListView, this class reimplements
    some of FormMixin due to it missing a super() call in get_context_data
    """
    search_form = None
    search_form_class = SearchForm
    search_filter = None
    initial = {}

    def get_initial(self):
        return self.initial.copy()

    def make_form(self, request):
        # Store the request so we can add success/failure messages.
        self.search_request = request
        # Searching uses GET at the moment. We create a bound form only if
        # any fields were passed, this prevents the form failing validation
        # when a user first hits a view we are mixed in to.
        if 'search' in request.GET:
            form = self.search_form_class(request.GET)
        else:
            form = self.search_form_class(self.get_initial())
        return form

    def get_queryset(self):
        # First handle any other processing that must be done
        qs = super(SearchFormMixin, self).get_queryset()
        if qs and self.search_filter:
            # If we have a queryset and a filter to apply to it, build a list
            # of fields to search and what to search them with.
            predicates = [
                (k + '__' + self.search_fields[k], self.search_filter) \
                for k in self.search_fields.keys()]
            # Build that into a list of Q filter objects
            qsfilter = [Q(x) for x in predicates]
            # Join them together with the or operator and pass them to filter
            newqs = qs.filter(reduce(operator.or_, qsfilter)).distinct()
            # If we get any items back, the search worked
            count = newqs.count()
            if count > 0:
                qs = newqs
                messages.success(
                    self.search_request, str(count) + ' item(s) found.')
            else:
                messages.warning(
                    self.search_request, 'Search returned no results.')
        return qs

    def get_context_data(self, **kwargs):
        # Add the search form to the page
        kwargs['search_form'] = self.search_form
        return super(SearchFormMixin, self).get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        self.search_form = self.make_form(request)
        if self.search_form.is_valid():
            # If the user entered any data, store it so get_queryset can
            # use it.
            self.search_filter = self.search_form.cleaned_data['search']
        return super(SearchFormMixin, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.search_form = self.make_form(request)
        if self.search_form.is_valid():
            self.search_filter = self.search_form.cleaned_data['search']
        return super(SearchFormMixin, self).post(request, *args, **kwargs)


class SetModelFieldMixin(object):
    """
    Mixin that can be used to set a value on a detail view (i.e. the view must
    have a self.get_object() function) on POST.
    """
    success_url = None

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")

    def get_field(self):
        try:
            return getattr(self, 'field')
        except AttributeError:
            raise ImproperlyConfigured("No field provided.")

    def get_value(self):
        try:
            return getattr(self, 'value')
        except AttributeError:
            raise ImproperlyConfigured("No value provided.")

    def set_value(self, *args, **kwargs):
        self.object = self.get_object()
        setattr(self.object, self.get_field(), self.get_value())
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def post(self, *args, **kwargs):
        return self.set_value(*args, **kwargs)
