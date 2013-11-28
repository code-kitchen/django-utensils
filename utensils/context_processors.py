# encoding: utf-8
from django.conf import settings


def pagination(request):
    """
    Provides a list of pagination sizes to the `pagination` template tag.
    
    Example settings config:
      PAGINATION_PAGE_SIZES = [20, 50, 100]
    """
    page_sizes = getattr(settings, 'PAGINATION_PAGE_SIZES', [20, 50, 100])
    return {
        'pagination_page_sizes': page_sizes,
    }
