import rest_framework.serializers
from rest_framework.serializers import Serializer, ModelSerializer
from app_student.models import Student, Hashtag, Record


class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = ['id','name','phone_number','address','address_detail']
        read_only_fields = ['id']

class HashtagSerializer(ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['id','record','tag']
        read_only_fields = ['id']

class RecordSerializer(ModelSerializer):
    student = StudentSerializer
    class Meta:
        model = Record
        fields = ['id','student','category','text']
        read_only_fields = ['id']

class CategorySerializer(Serializer):
    category_name = rest_framework.serializers.CharField(max_length=255)