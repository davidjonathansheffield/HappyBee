import datetime

from django.db import models


class BaseQuerySet(models.QuerySet):
    pass


class BaseManager(models.Manager):
    pass


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
