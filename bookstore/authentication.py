from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token

class CustomTokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'

    def authenticate(self, request):
        auth = request.headers.get('Authorization')

        if not auth:
            return None

        auth_parts = auth.split()

        if len(auth_parts) != 2 or auth_parts[0].lower() != self.keyword.lower():
            return None

        token = auth_parts[1]

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        return (token.user, token)
