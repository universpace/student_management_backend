from django.contrib import admin
from app_student.models import Hashtag, Record, Student, CategoryMeta
# Register your models here.
class HashtagAdmin(admin.ModelAdmin):
    pass
class RecordAdmin(admin.ModelAdmin):
    pass
class StudentAdmin(admin.ModelAdmin):
    pass
class RecordNHashtagAdmin(admin.ModelAdmin):
    pass
class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Hashtag,HashtagAdmin)
admin.site.register(Record,RecordAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(CategoryMeta,CategoryAdmin)