from django.db import models


class BaseModel(models.Model):
    """
    Стандартная абстрактная модель
    """

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
