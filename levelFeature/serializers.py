from rest_framework import serializers
from .models import LevelReading, Livestream


class LevelReadingSerializer(serializers.ModelSerializer):

    class Meta:
        model = LevelReading
        fields = '__all__'


class LivestreamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Livestream
        fields = '__all__'