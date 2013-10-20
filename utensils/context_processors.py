# encoding: utf-8
from django.conf import settings


def pagination(request):
    return {
        'pagination_page_sizes': settings.PAGINATION_PAGE_SIZES,
    }
