from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from logger import logger

from .tasks import notify_services_of_new_user

class RegisterView(APIView):
    def post(self, request):
        logger.info(f"Начало процесса регистрации. Данные запроса: {request.data}")
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                logger.debug(f"Создан пользователь с ID {user.id}. Email: {user.email}")
                
                # Асинхронно уведомляем другие сервисы
                notify_services_of_new_user.delay(user.id)
                logger.info(f"Запущена задача уведомления сервисов о новом пользователе {user.id}")
                
                logger.info(f"Успешная регистрация пользователя {user.id}. Сгенерированы токены")
                return Response({
                    'user': serializer.data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.exception(f"Критическая ошибка при регистрации пользователя. Данные: {request.data}")
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        logger.warning(f"Ошибка валидации при регистрации. Ошибки: {serializer.errors}, Данные: {request.data}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ValidateTokenView(APIView):
    def post(self, request):
        token = request.data.get('token')
        if not token:
            logger.warning("Попытка валидации токена без предоставления токена")
            return Response({'detail': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            logger.info(f"Успешная валидация токена для пользователя {user_id}")
            return Response({'valid': True, 'user_id': user_id}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Ошибка валидации токена: {str(e)}. Предоставленный токен: {token[:10]}...")
            return Response({'valid': False, 'detail': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
