from django.conf import settings
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin

from .models import DdosSettings
from .redis_adapter import RedisAdapter


class RateLimitMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        self.get_response = get_response
        self.redis_adapter = self.initialize_redis_adapter()

    def initialize_redis_adapter(self):
        """Initialize RedisAdapter with settings from the database or defaults."""
        timeout = self.get_timeout()
        max_requests = self.get_max_requests()

        return RedisAdapter(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            timeout=timeout,
            max_requests=max_requests,
        )

    def __call__(self, request):
        ip = self.get_client_ip(request)
        endpoint = request.path

        rate_limit = DdosSettings.objects.filter(endpoint=endpoint).first()

        if not rate_limit:
            rate_limit = DdosSettings.objects.filter(is_default=True).first()

        if rate_limit:
            self.redis_adapter.max_requests = rate_limit.max_requests
            self.redis_adapter.timeout = rate_limit.timeout
        else:
            self.redis_adapter.max_requests = self.get_max_requests()
            self.redis_adapter.timeout = self.get_timeout()

        self.redis_adapter.set_ip_mask(ip)

        if self.redis_adapter.count_keys(ip) > self.redis_adapter.max_requests:
            return HttpResponseForbidden("You are blocked due to too many requests.")

        response = self.get_response(request)
        return response

    def get_max_requests(self):
        """Retrieve max requests from admin settings or defaults."""
        admin_settings = DdosSettings.objects.filter(is_default=True).first()
        if admin_settings:
            return admin_settings.limit
        return getattr(settings, "REDIS_MAX_REQUESTS", 100)

    def get_timeout(self):
        """Retrieve timeout from admin settings or defaults."""
        admin_settings = DdosSettings.objects.filter(is_default=True).first()
        if admin_settings:
            return admin_settings.time_window
        return getattr(settings, "REDIS_TIMEOUT", 5 * 60)

    def get_client_ip(self, request):
        """Gets the client IP address from the request."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
