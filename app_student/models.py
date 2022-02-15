from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=255,blank=True)
    phone_number = models.CharField(max_length=11,blank=True)
    address = models.CharField(max_length=255, blank=True)
    address_detail = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Record(models.Model):
    student = models.ForeignKey(Student,models.CASCADE)
    category = models.CharField(max_length=255)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.student.name}의{self.category}에 관한 기록'

class Hashtag(models.Model):
    record = models.ManyToManyField(Record,related_name='hashtag')
    tag = models.CharField(max_length=255,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.record.__str__()}의{self.tag}'

class CategoryMeta(models.Model):
    category_name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_name