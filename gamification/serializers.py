from rest_framework import serializers
from gamification.models import Challenge, ChallengeUser


class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = '__all__'

    type = serializers.CharField(source='get_type_display')
    period = serializers.CharField(source='get_period_display')
    user_challenge = serializers.SerializerMethodField()

    def get_user_challenge(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            try:
                challenge_user = ChallengeUser.objects.get(challenge=obj, user=request.user)
                return {
                    'completed': challenge_user.completed,
                    'joined': True,
                    'date': challenge_user.date
                }
            except ChallengeUser.DoesNotExist:
                return {
                    'completed': False,
                    'joined': False,
                    'date': None
                }
        return None
