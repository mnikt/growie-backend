from rest_framework import serializers
from gamification.models import Challenge


class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = '__all__'

    type = serializers.CharField(source='get_type_display')
    period = serializers.CharField(source='get_period_display')
