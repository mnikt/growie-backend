import json

from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone

from gamification.auth import UserAuthentication
from gamification.models import Challenge, User, ChallengeUser, QuizAnswer, Event, Quiz, EventUser, Pets
from gamification.serializers import ChallengeSerializer, EventSerializer, QuizSerializer


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

    def filter_queryset(self, queryset):
        return queryset.filter(end_date__gte=timezone.now().date(), start_date__lte=timezone.now().date())


class ChallengesDetailsApiView(RetrieveAPIView):
    authentication_classes = [UserAuthentication]

    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer


class ChallengesJoinApiView(APIView):
    authentication_classes = [UserAuthentication]

    def post(self, request, pk):
        if ChallengeUser.objects.filter(challenge_id=pk, user=request.user).exists():
            return Response(status=400, data={"joined": True})
        else:
            ChallengeUser(challenge_id=pk, user=request.user).save()
            return Response(status=200, data={"joined": True})


class ChallengesCompleteApiView(APIView):
    authentication_classes = [UserAuthentication]

    def post(self, request, pk):
        try:
            challenge = ChallengeUser.objects.get(challenge_id=pk, user=request.user)
            challenge.completed = True
            challenge.save()
        except ChallengeUser.DoesNotExist:
            return Response(status=404, data={'error': 'Challenge not found'})
        return Response(status=200, data={'completed': True})


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


class QuizListView(ListView):
    model = Quiz
    ordering = ['-date']


class QuizCreateView(CreateView):
    model = Quiz
    fields = '__all__'
    success_url = '/gamification/quizzes'


class QuizDetailsView(DetailView):
    model = Quiz
    fields = '__all__'


class QuizUpdateView(UpdateView):
    model = Quiz
    fields = '__all__'

    def get_success_url(self):
        return f'/gamification/quizzes/details/{self.object.pk}'


class EventsListApiView(ListAPIView):
    authentication_classes = [UserAuthentication]

    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventsDetailsApiView(RetrieveAPIView):
    authentication_classes = [UserAuthentication]

    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventsJoinApiView(APIView):
    authentication_classes = [UserAuthentication]

    def post(self, request, pk):
        try:
            if EventUser.objects.filter(event_id=pk).count() < Event.objects.get(pk=pk).limit:
                EventUser.objects.get_or_create(event_id=pk, user=request.user)
                return Response(status=200, data={"joined": True})
        except Event.DoesNotExist:
            return Response(status=404, data={"error": "Event not found"})
        return Response(status=400, data={"joined": False})


class QuizListApiView(ListAPIView):
    authentication_classes = [UserAuthentication]

    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    
    def filter_queryset(self, queryset):
        return queryset.filter(date=timezone.now().date())


class QuizAnswerApiView(APIView):
    authentication_classes = [UserAuthentication]

    def post(self, request, pk):
        try:
            quiz = Quiz.objects.get(pk=pk)
            if QuizAnswer.objects.filter(quiz=quiz, user=request.user).exists():
                return Response(status=400, data={"error": "You have already answered this quiz"})
            correct = quiz.correct_answer == request.data['answer']
            QuizAnswer.objects.create(quiz=quiz, user=request.user, correct=correct)
            return Response(status=200, data={"correct": correct})
        except Quiz.DoesNotExist:
            return Response(status=404, data={"error": "Quiz not found"})


class RankingView(APIView):
    authentication_classes = [UserAuthentication]

    @staticmethod
    def get_users_points(user):
        quizzes_points = QuizAnswer.objects.filter(correct=True, user=user).aggregate(sum=Sum('quiz__points'))['sum'] or 0
        challenges_points = ChallengeUser.objects.filter(completed=True, user=user).aggregate(sum=Sum('challenge__points'))['sum'] or 0
        return quizzes_points + challenges_points

    def get(self, request):
        data = [{
            'id': user.id,
            'name': user.name,
            'points': self.get_users_points(user)
            } for user in User.objects.all()
        ]

        data.sort(key=lambda x: x['points'], reverse=True)
        return Response(data)


class PetImageView(APIView):
    authentication_classes = [UserAuthentication]

    def get(self, request):
        pet = Pets.objects.filter(user=request.user)

        if pet.exists():
            return Response({'image': pet.first().image.url})
        return Response(status=404, data={'error': 'No pet found for this user'})

    def post(self, request):
        if 'image' not in request.FILES:
            return Response(status=400)

        pet = Pets.objects.filter(user=request.user).first()

        if pet is None:
            pet = Pets.objects.create(user=request.user, image=request.FILES['image'])
        else:
            pet.image = request.FILES['image']
            pet.save()
        return Response(status=200, data={'image': pet.image.url})
