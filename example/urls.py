from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

from django.contrib import admin
admin.autodiscover()

from . import views


urlpatterns = patterns('',
    url(r'^admin/',
        include(admin.site.urls)),
    url(r'^$',
        RedirectView.as_view(url='/books/')),
    url(r'^books/$',
        views.BookListView.as_view(),
        name='book_list'),
    url(r'^books/(?P<pk>\d+)/edit/$',
        views.BookUpdateView.as_view(),
        name='book_edit'),
    url(r'^books/(?P<pk>\d+)/toggle-in-stock/$',
        views.ToggleNotInStockView.as_view(),
        name='book_toggle_in_stock'),
)
