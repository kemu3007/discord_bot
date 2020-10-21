from django.db import models


class Ohayou(models.Model):
    text = models.TextField("内容")