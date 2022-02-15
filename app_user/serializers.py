from django.contrib.auth import get_user_model
from rest_framework.serializers import Serializer, ModelSerializer
User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','username','name','created_at','updated_at']