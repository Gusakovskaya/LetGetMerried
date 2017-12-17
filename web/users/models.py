from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField
from django.db import models


class User(AbstractUser):
    twitter_handle = models.CharField(max_length=256)
    statistics = JSONField(null=True)
