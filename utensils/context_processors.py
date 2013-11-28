# encoding: utf-8
from django.conf import settings


def pagination(request):
    """
    Used by the `pagination` template tag.
    
    Example settings config:
      PAGINATION_PAGE_SIZES = [20, 50, 100]
    """
    return {
        'pagination_page_sizes': settings.PAGINATION_PAGE_SIZES,
    }
