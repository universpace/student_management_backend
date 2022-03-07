import django_filters.filterset as filterset

from app_student.models import Student, Record


class StudentFilterSet(filterset.FilterSet):
    name = filterset.CharFilter(field_name='name', lookup_expr='icontains')
    class Meta:
        model = Student
        fields = ['name']


class RecordFilterSet(filterset.FilterSet):
    student_name = filterset.CharFilter(field_name='student__name', lookup_expr='icontains')
    class Meta:
        model = Record
        fields = ['student','category', 'student_name']