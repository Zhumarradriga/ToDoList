from rest_framework import viewsets, permissions
from todo.models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)