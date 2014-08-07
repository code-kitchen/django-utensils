from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from .views import BookListView, SetNotInStockView


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^book/$', BookListView.as_view(), name='book_list'),
    url(r'^book/(?P<pk>\d+)/set-not-in-stock/$', SetNotInStockView.as_view(), name='book_not_in_stock'),
)
