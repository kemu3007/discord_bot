from django.db import models

from bot_backend.models import TimeStampModel


class Ohayou(TimeStampModel):
    text = models.TextField("内容")


class HoloduleReminder(TimeStampModel):
    channel_code = models.CharField("チャンネルID", max_length=20, unique=True, primary_key=True)
    channel_name = models.CharField("チャンネル名", max_length=2000)
