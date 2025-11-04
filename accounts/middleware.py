from django.contrib.auth import get_user_model
from django.utils.deprecation import MiddlewareMixin

from .jwt import verify_token, COOKIE_NAME


User = get_user_model()


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # If already authenticated via session, keep it
        if getattr(request, "user", None) and request.user.is_authenticated:
            return None

        token = None
        # Prefer Authorization header if present
        auth = request.META.get("HTTP_AUTHORIZATION", "")
        if auth.lower().startswith("bearer "):
            token = auth.split(" ", 1)[1].strip()
        elif COOKIE_NAME in request.COOKIES:
            token = request.COOKIES.get(COOKIE_NAME)

        if not token:
            return None

        data = verify_token(token)
        if not data:
            return None

        sub = data.get("sub")
        try:
            user_id = int(sub)
        except (TypeError, ValueError):
            return None
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

        # Attach the authenticated user for this request
        request.user = user
        return None
