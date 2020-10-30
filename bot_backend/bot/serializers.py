from rest_framework import serializers

from bot.models import HoloduleReminder, Ohayou


class OhayouSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ohayou
        read_only_fields = ["id"]
        fields = ["id", "text"]


class HoloduleReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = HoloduleReminder
        fields = ["channel_code", "channel_name"]