from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from gamification.models import User


class UserAuthentication(BaseAuthentication):
    def authenticate(self, request):
        user_id = request.headers.get('Authentication')

        if not user_id:
            return None

        try:
            user = User.objects.get(id=user_id)
            return user, None
        except (User.DoesNotExist, ValueError):
            raise AuthenticationFailed('Invalid user ID')
