from apps.requests.models import RequestEntry
from django.core.urlresolvers import reverse
from django.conf import settings


class RequestMiddleware(object):
    """ saves info about all requests into DB. """

    def process_request(self, request):
        # we shouldn't save request if it is that fetches new requests
        if reverse('requests_api') in request.path and request.is_ajax():
            return

        r = RequestEntry()
        r.method = request.method
        r.absolute_path = request.build_absolute_uri()
        r.is_ajax = request.is_ajax()
        if request.path.startswith(settings.STATIC_URL):
            r.priority = 0
        r.save()
