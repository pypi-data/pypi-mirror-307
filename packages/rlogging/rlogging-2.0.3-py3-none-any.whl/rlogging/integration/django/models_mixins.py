from django.db import models


class BaseEntityAbstractModel(models.Model):
    """Базовый-абстрактный класс для сущностей НСИ.

    Класс реализует поля "created_at" и "updated_at" и связную с ними логику.
    """

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='DateTime of creating')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='DateTime of updating')

    class Meta:
        abstract = True
