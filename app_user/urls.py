from django.urls import path
from rest_framework.routers import SimpleRouter
from app_user.views import UserCRUD
router = SimpleRouter()
router.register(prefix='',viewset=UserCRUD)

urlpatterns = []
urlpatterns += router.urls