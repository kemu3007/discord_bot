from rest_framework import serializers

from bot.models import Ohayou


class OhayouSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ohayou
        read_only_fields = ["id"]
        fields = ["id", "text"]
