from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import EmailValidator
from django.db import models
from django.utils import timezone


class AbstractBaseModel(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False, unique=True)
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    class Meta:
        abstract = True

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.id}>'


class CustomUserManager(UserManager):
    use_in_migrations = True

    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('must have user email')
        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, username):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username
        )
        user.is_active = True
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(PermissionsMixin, AbstractBaseUser, AbstractBaseModel):

    objects = CustomUserManager()
    email = models.EmailField(max_length=255, unique=True, validators=[EmailValidator], verbose_name='이메일')
    username = models.CharField(max_length=150,unique=True)
    name = models.CharField(max_length=150,blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']  # used only on createsuperuser

    class Meta:
        verbose_name_plural = '유저_목록'
        ordering = ['date_joined', ]

    @property
    def is_django_user(self):
        return self.has_usable_password()