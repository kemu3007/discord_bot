from django.db import models


class TimeStampModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField("作成日時", auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField("最終更新日時", auto_now=True, null=True, blank=True)
