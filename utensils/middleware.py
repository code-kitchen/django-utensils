# encoding: utf-8
from django.conf import settings
from django.http import HttpResponseForbidden


HIDDEN_SITE_SECRET = getattr(settings, 'HIDDEN_SITE_SECRET', None)


class HiddenSiteMiddleware(object):
    """
    Blocks pages unless a cookie or GET parameter is present.
    E.g. /some/path/?secret (where 'secret' is HIDDEN_SITE_SECRET)
    """
    COOKIE_NAME = 'hidden_site_secret'

    def process_request(self, request):
        if (self.COOKIE_NAME in request.COOKIES or
                request.GET.has_key(HIDDEN_SITE_SECRET)):
            return None
        return HttpResponseForbidden("ACCESS DENIED")

    def process_response(self, request, response):
        if (not self.COOKIE_NAME in request.COOKIES
                and request.GET.has_key(HIDDEN_SITE_SECRET)):
            response.set_cookie(self.COOKIE_NAME, True, max_age=365*24*60*60)
        return response
