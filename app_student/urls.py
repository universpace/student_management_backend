from django.urls import path, include
from rest_framework.routers import SimpleRouter
from app_student.views import StudentCRUDViewSet, RecordCRUDView, GetCategoryMeta
router = SimpleRouter()
router.register(r'student',StudentCRUDViewSet)
router.register(r'record',RecordCRUDView)

urlpatterns = [
    path('category/',GetCategoryMeta.as_view()),
    path('',include(router.urls))
]
