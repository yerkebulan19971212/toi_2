from django.db import models


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-
    updating ``created`` and ``modified`` fields.
    """
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создание")
    modified = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        abstract = True


class NameModel(TimeStampedModel):
    """
    """
    name_kz = models.CharField(
        max_length=255, default='', blank=True, null=True)
    name_ru = models.CharField(
        max_length=255, default='', blank=True, null=True)
    name_en = models.CharField(
        max_length=255, default='', blank=True, null=True)

    class Meta:
        abstract = True


class AbstractQuerySet(models.QuerySet):

    def get_all_active(self):
        return self.filter(is_active=True)

    def is_active(self):
        return self.filter(is_active=True)

    def not_deleted(self):
        return self.filter(deleted__isnull=True)
