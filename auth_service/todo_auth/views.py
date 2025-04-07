from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


from .tasks import notify_services_of_new_user

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            notify_services_of_new_user.delay(user.id)  # Асинхронно уведомляем другие сервисы
            return Response({
                'user': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ValidateTokenView(APIView):
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'detail': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            access_token= AccessToken(token)
            user_id= access_token['user_id']
            return Response({'valid': True, 'user_id': user_id}, status=status.HTTP_200_OK)
        except Exception as e:
            return  Response({'valid': False, 'detail': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
