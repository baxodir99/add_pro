from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):

  def create_user(self, username, email, password=None):
    if not email:
      raise ValueError('User must have an email address')
    if not username:
      raise ValueError('User must have a username')
    
    user = self.model(username = username, email = self.normalize_email(email))
    user = self.model(username = username)
    user.set_password(password)
    user.save(using = self._db)
    return user

  def create_superuser(self, username, email, password):
        if username is None:
            raise TypeError('phone is required to phone')
        if email is None:
            raise ValueError("User must have an email")
        if password is None:
            raise TypeError('Password is required to phone')
        user = self.create_user(username=username,email=email, password=password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length = 30,
        unique = True
    )
    email = models.EmailField(
        max_length = 60,
        unique = True
    )
    first_name = models.CharField(
        max_length = 30,
        null = True,
        blank = True
    )
    last_name = models.CharField(
        max_length = 30,
        null = True,
        blank = True
    )
    phone = models.CharField(
        max_length=30, null=True, blank=True, unique=True)
    date_joined = models.DateField(auto_now_add = True)
    is_staff = models.BooleanField(
        default = False
    )
    is_superuser = models.BooleanField(
        default = False
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return f'{self.id} {self.username}'