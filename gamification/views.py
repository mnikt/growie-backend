import json

from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from gamification.auth import UserAuthentication
from gamification.models import Challenge, User, ChallengeUser, QuizAnswer, Event
from gamification.serializers import ChallengeSerializer


@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    data = json.loads(request.body)

    if "name" not in data:
        return JsonResponse({'error': 'No name provided'}, status=400)

    user = User.objects.create(name=data["name"])

    return JsonResponse({'name': user.name, 'id': user.id})


class ChallengesListView(ListView):
    model = Challenge
    ordering = ['name']

    def get_ordering(self):
        order_by = self.request.GET.get('order_by', 'name')
        direction = self.request.GET.get('direction', 'asc')
        if direction == 'desc':
            return f'-{order_by}'
        return order_by

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_by'] = self.request.GET.get('order_by', 'name')
        context['direction'] = self.request.GET.get('direction', 'asc')
        return context


class ChallengesCreateView(CreateView):
    model = Challenge
    fields = '__all__'
    success_url = '/gamification/challenges'


class ChallengesDetailsView(DetailView):
    model = Challenge
    fields = '__all__'


class ChallengesUpdateView(UpdateView):
    model = Challenge
    fields = '__all__'

    def get_success_url(self):
        return f'/gamification/challenges/details/{self.object.pk}'


class ChallengesListApiView(ListAPIView):
    authentication_classes = [UserAuthentication]

    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer


class ChallengesDetailsApiView(RetrieveAPIView):
    authentication_classes = [UserAuthentication]

    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer


class ChallengesJoinApiView(APIView):
    authentication_classes = [UserAuthentication]

    def post(self, request, pk):
        if ChallengeUser.objects.filter(challenge_id=pk, user=request.user).exists():
            return Response(status=400)
        else:
            ChallengeUser(challenge_id=pk, user=request.user).save()
            return Response(status=200)


class ChallengesCompleteApiView(APIView):
    authentication_classes = [UserAuthentication]

    def post(self, request, pk):
        try:
            challenge = ChallengeUser.objects.get(challenge_id=pk, user=request.user)
            challenge.completed = True
            challenge.save()
        except ChallengeUser.DoesNotExist:
            return Response(status=404)
        return Response(status=200)


class PointsApiView(APIView):
    authentication_classes = [UserAuthentication]

    def get(self, request):
        challenges = [{'points': cu.challenge.points, 'date': cu.date, 'name': str(cu.challenge)}
                      for cu in ChallengeUser.objects.filter(user=request.user, completed=True)]

        quizzes = [{'points': qa.quiz.points, 'date': qa.quiz.date, 'name': str(qa.quiz)}
                   for qa in QuizAnswer.objects.filter(user=request.user, correct=True)]

        history = challenges + quizzes

        return Response({'total': sum(item['points'] for item in history), 'history':history})


class EventListView(ListView):
    model = Event
    ordering = ['-date']


class EventCreateView(CreateView):
    model = Event
    fields = '__all__'
    success_url = '/gamification/events'


class EventsDetailsView(DetailView):
    model = Event
    fields = '__all__'


class EventsUpdateView(UpdateView):
    model = Event
    fields = '__all__'

    def get_success_url(self):
        return f'/gamification/events/details/{self.object.pk}'


# class ChallengesListApiView(ListAPIView):
#     authentication_classes = [UserAuthentication]
#
#     queryset = Challenge.objects.all()
#     serializer_class = ChallengeSerializer
#
#
# class ChallengesDetailsApiView(RetrieveAPIView):
#     authentication_classes = [UserAuthentication]
#
#     queryset = Challenge.objects.all()
#     serializer_class = ChallengeSerializer
#
#
# class ChallengesJoinApiView(APIView):
#     authentication_classes = [UserAuthentication]
#
#     def post(self, request, pk):
#         if ChallengeUser.objects.filter(challenge_id=pk, user=request.user).exists():
#             return Response(status=400)
#         else:
#             ChallengeUser(challenge_id=pk, user=request.user).save()
#             return Response(status=200)