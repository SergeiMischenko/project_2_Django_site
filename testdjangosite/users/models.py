from django.contrib.auth.models import AbstractUser
from django.db import models


def get_user_path(instance, filename):
    return f"users/photos/{instance.username}/{filename}"


class User(AbstractUser):
    photo = models.ImageField(
        upload_to=get_user_path, blank=True, null=True, verbose_name="Фото"
    )
    date_birth = models.DateTimeField(
        blank=True, null=True, verbose_name="Дата рождения"
    )
