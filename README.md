# django-utensils

A collection of reusable components to help build Django projects.

## Installation

To install the latest stable release:

    pip install django-utensils

To get the latest dev version, install directly form GitHub like so:

    pip install -e git://github.com/code-kitchen/django-utensils.git#egg=django-utensils

Many of the template tags require the `request` object. You need to add 'django.template.context_processors.request' (Django 1.6 and 17) or 'django.template.context_processors.request' (Django 1.8) to the template context processors in your settings.

To use the `AddressedModel` you will need to add `countries_plus` to your `INSTALLED_APPS` setting.

## Forms

### `SearchForm`

Generic search form that can be used on any page.

Used by `viewmixins.SearchFormMixin`.


### `UniqueModelFieldsMixin`

Mixin that enforces unique fields on ModelForm form fields.

Must be left of ModelForm when defining the form class (see https://code.djangoproject.com/ticket/13075).

There are two ways to list your unique fields depending on whether or not you want case insensitivity.

```python
unique_fields = ['name', 'username']
unique_fields = ['name',  {'field': 'username', 'case_insensitive': True}]
```

## Middleware

### Hidden site

By adding `utensils.middleware.HiddenSiteMiddleware` to your `MIDDLEWARE_CLASSES` you can prevent people from viewing your site unless they use a query string parameter. The parameter is not needed for subsequent visits (unless cookies are cleared). This is a quick and simple method to keep prying eyes off your staging server for example. Provide the parameter name in the settings variable `HIDDEN_SITE_SECRET`.

For example:

```python
MIDDLEWARE_CLASSES += ('utensils.middleware.HiddenSiteMiddleware',)
HIDDEN_SITE_SECRET = 'whisky'
```

Using the built-in development server browsing to http://localhost/ will give the message "ACCESS DENIED". Browing to http://localhost/?whisky will succeed. Subsequent visits to http://localhost/ (no `?whisky`) with the same browser will succeed until cookies are cleared or the cookie expires (currently set to a year).

## View mixins

Collection of mixins for class-based views.

### List view pagination

The `PaginateMixin` returns the paginate by setting used by the pagination template tag `{% pagination %}` so the Django `ListView` functions can use it.

You will need to add `utensils.context_processors.pagination` to your context processors for the template tag to work. Set `settings.PAGINATION_PAGE_SIZES` to control the page size, if not set the default `[20, 50, 100]` is used.

### List view ordering

The `OrderByMixin` allows easy ordering of list views. By including it the template tag (`{% order_by 'field_name' %}`) is given sorting context variables to work with. `get_queryset` is overidden to make use of these and order the object list.

### Generic single-field search

The `SearchFormMixin` provides a handy way to add search to list views. Add the `search_form` manually in your template or use the included fragment `{% include 'fragments/_search.html' %}`.

Specify the fields you wish to search on, and how, by including a `search_fields` dictionary on your view like so:

```python
class CustomerListView(SearchFormMixin, ListView):
    model = Customer
    search_fields = {
        'user__email':  'icontains',
        'first_name':   'icontains',
        'last_name':    'icontains',
        'postal_code':  'icontains',
    }
```

### `MessageMixin`

By including and providing `success_message` and/or `error_message` attributes on your view class, messages will be added automatically to the request objects on events suchs as valid and invalid forms and formsets, object deletion etc.

### `PermissionRequiredMixin`

This mixin verfies the user is logged in and has the required permissions to access the view. It's a modified version of the django-braces mixin with an added bypass. Setting `permission_required = False` allows you to skip the check whilst keeping the mixin in a base view used across a project, for example.

Settings:

 * `permission_required` - the permission to check for or False to skip check
 * `login_url` - the login url of site
 * `redirect_field_name` - defaults to "next"
 * `raise_exception` - defaults to False - raise 403 if set to True

### `RedirectToNextMixin`

If a `next` query string parameter is preset on a `post()` call it is assigned to the instance `success_url`.

### `StaffViewMixin`

Combines `MessageMixin`, `RedirectToNextMixin`, `StaffuserRequiredMixin` (from django-brances), `PermissionRequiredMixin` to create a useful mixin that can be used on all staff views.

## Views

### `BaseListView`

This view combines the pagination, order by and search mixins and adds an optional query set filter description that your templates can use.

```python
class ActiveCustomerList(BaseListView):
    filter_description = u"Active"
    queryset = Customer.active.all()
```
    
```html
{% block content %}
  <h2>
    {% if filter_description %}
      {{ filter_description|title }} customers
    {% else %}
      Customers
    {% endif %}
  </h2>
  <!-- more template -->
{% end block %}
```

Yields:

```html
  <h2>Active customers<h2>
  <!-- more template -->
```

### `SetModelFieldView`

This view can be used to set the value of a field on a model instance. GET will display a template (and should be used as a confirmation page) and the value will be set on POST. The view uses `django.views.generic.detail.BaseDetailView` to provide `get_object()`.

```python
class CustomerInactiveView(SetModelFieldView):
    """
    Ask the user if they're sure they want to make the customer inactive. If
    they confirm by submitting the form set is_active to False and save.
    """
    model = Customer
    field = 'is_active'
    value = False
    template_name = "customers/customer_inactive.html"
```

If you require more control and want to introduce some logic when selecting the value or field to alter you can override `get_field()` and `get_value()` instead of setting the `field` and `value` class attributes.

## Storage

### S3

The `storage` modules provides a way to easily store static or media files on Amazon S3.

To use you will need to update your `settings` with the appropriate configuration, something like this:

```python
AWS = {
    'STATIC': {
        'location': 'static',           # AWS_LOCATION
        'querystring_auth': False,      # AWS_QUERYSTRING_AUTH
        'default_acl': 'public-read',   # AWS_DEFAULT_ACL
    },
    'MEDIA': {
        'location': 'media',            # AWS_LOCATION
        'querystring_auth': True,       # AWS_QUERYSTRING_AUTH
        'default_acl': 'private',       # AWS_DEFAULT_ACL
    },
}

AWS_ACCESS_KEY_ID = 'XXXXXXXXXXXXXXXXXXXX'
AWS_SECRET_ACCESS_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
AWS_STORAGE_BUCKET_NAME = 'bucket'
AWS_PRELOAD_METADATA = True
AWS_S3_SECURE_URLS = False

STATICFILES_STORAGE = 'utensils.storage.StaticRootS3BotoStorage'
DEFAULT_FILE_STORAGE = 'utensils.storage.MediaRootS3BotoStorage'
```

## Miscellaneous utils

There are utility functions in the `utils` module that deal with a range of things. Some are used by other parts of the library.
