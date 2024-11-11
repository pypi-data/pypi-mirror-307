from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse

from rlogging import HttpLoggerAdapter


class DjangoLoggerAdapter(HttpLoggerAdapter):
    def request(self, request: WSGIRequest, *args, **kwargs):
        kwargs.setdefault('stacklevel', 5)

        kwargs['extra'] = kwargs.get('extra', {})
        kwargs['extra'].update({'django': {'path': request.path, 'view_func': request.resolver_match}})

        return super().request(
            request.build_absolute_uri(),
            request.method,
            *args,
            **kwargs,
        )

    def response(self, response: HttpResponse, *args, **kwargs):
        kwargs.setdefault('stacklevel', 5)
        return super().response(response.status_code, *args, **kwargs)
