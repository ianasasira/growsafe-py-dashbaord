from .mixins import RequestMiddleware

class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_middleware = RequestMiddleware(get_response)

    def __call__(self, request):
        request.company = None
        if request.user.is_authenticated and request.user.company:
            request.company = request.user.company
        return self.request_middleware(request)
