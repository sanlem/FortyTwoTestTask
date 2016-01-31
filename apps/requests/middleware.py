from apps.requests.models import RequestEntry


class RequestMiddleware(object):
    """ saves info about all requests inti DB. """

    def process_request(self, request):
        r = RequestEntry()
        r.method = request.method
        r.absolute_path = request.build_absolute_uri()
        r.is_ajax = request.is_ajax()
        r.save()
        return None
