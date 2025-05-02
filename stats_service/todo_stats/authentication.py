import requests
from rest_framework.authentication import BaseAuthentication
from  rest_framework.exceptions import AuthenticationFailed

class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header=request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        token=auth_header.split(' ')[1]
        response=requests.post('http://authservice:8000/api/auth/token/verify/', json={'token':token})

        if response.status_code!=200 or not response.json().get('valid'):
            raise AuthenticationFailed('Invalid token')
        user_id=response.json().get('user_id')
        return (user_id, None)