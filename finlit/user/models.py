from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    GUEST = 0
    STUDENT = 1
    TEACHER = 2
    COUNSELLOR = 3
    ADMIN = 4
    ROLES = (
        (GUEST, 'Guest'),
        (STUDENT, 'Student'),
        (TEACHER, 'Teacher'),
        (COUNSELLOR, 'Counsellor'),
        (ADMIN, 'Admin')
    )
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=15, blank=True, validators=[MinLengthValidator(8)])
    is_verified_email = models.BooleanField(default=False)

    role = models.SmallIntegerField(default=GUEST, choices=ROLES)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
