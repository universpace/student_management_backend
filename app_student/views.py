from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.filters import SearchFilter

from app_student.filters import StudentFilterSet, RecordFilterSet
from app_student.models import Student, Record, Hashtag, CategoryMeta
from app_student.serializers import StudentSerializer, RecordSerializer, HashtagSerializer, CategorySerializer

User = get_user_model()



class StudentCRUDViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (AllowAny,)
    filterset_class = StudentFilterSet


class RecordCRUDView(ModelViewSet):
    queryset = Record.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RecordSerializer
    filterset_class = RecordFilterSet


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        for row in data:
            id = row.get('id')
            tags = Hashtag.objects.filter(record=id).values_list('tag',flat=True)
            row.update({'hashtag':tags})

        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        tags = Hashtag.objects.filter(record=instance.pk).values_list('tag', flat=True)
        data.update({'hashtag':tags})
        return Response(data)


    def create(self, request, *args, **kwargs):
        data = request.data
        hashtag = data.get('hashtag','').split(',')
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, hashtag)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, hashtag):
        instance = serializer.save()
        for tag in hashtag:
            tag_data = {
                'tag':tag,
                'record':[instance.pk,]
            }
            tagSerializer = HashtagSerializer(data=tag_data)
            tagSerializer.is_valid(raise_exception=True)
            tagSerializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        hashtag = request.data.get('hashtag', '').split(',')
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer, hashtag)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        data = serializer.data
        tags = Hashtag.objects.filter(record=instance.pk).values_list('tag',flat=True)
        data.update({'hashtag':tags})
        return Response(data)

    def perform_update(self, serializer, hashtag):

        instance = serializer.save()
        exist_tags = Hashtag.objects.filter(record=instance.pk)
        for tag in exist_tags:
            tag.delete()
        for tag in hashtag:
            tag_data = {
                'tag':tag,
                'record':[instance.pk,]
            }
            tagSerializer = HashtagSerializer(data=tag_data)
            tagSerializer.is_valid(raise_exception=True)
            tagSerializer.save()


class CategoryMetaAPIView(APIView):
    def get(self, request):
        return Response(CategoryMeta.objects.all().values('id','category_name'),status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = CategorySerializer(data=data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        __ = CategoryMeta.objects.create(category_name=data.get('category_name'))
        return Response(status=status.HTTP_201_CREATED)

class DeleteCategoryMetaAPIView(APIView):

    @transaction.atomic
    def delete(self, request, pk):
        pk = self.kwargs['pk']
        target_category = CategoryMeta.objects.filter(id=pk)
        if not target_category:
            return Response(data={'msg':'해당하는 카테고리가 존재하지 않습니다.'},status=status.HTTP_400_BAD_REQUEST)
        for category in target_category:
            category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
