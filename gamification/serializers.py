from rest_framework import serializers
from gamification.models import Challenge, ChallengeUser, Event, EventUser, QuizAnswer, Quiz


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


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

    user_joined = serializers.SerializerMethodField()
    joined_number = serializers.SerializerMethodField()

    def get_user_joined(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return EventUser.objects.filter(event=obj, user=request.user).exists()
        return False

    def get_joined_number(self, obj):
        return EventUser.objects.filter(event=obj).count()


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'

    answered = serializers.SerializerMethodField()
    correct = serializers.SerializerMethodField()

    def get_answered(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return QuizAnswer.objects.filter(quiz=obj, user=request.user).exists()
        return False

    def get_correct(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            try:
                return QuizAnswer.objects.get(quiz=obj, user=request.user).correct
            except QuizAnswer.DoesNotExist:
                return False
        return False
