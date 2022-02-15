from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from app_user.serializers import UserSerializer
User = get_user_model()

class UserCRUD(ModelViewSet):
    permission_classes = (AllowAny,IsAuthenticated)
    queryset = User.objects.all()
    serializer_class = UserSerializer