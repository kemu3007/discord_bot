from rest_framework import serializers
from bot.models import Ohayou

from bot_backend import models


class OhayouSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ohayou

        read_only_fields = [
            "id"
        ]

        fields = [
            'id',
            'text'
        ]
