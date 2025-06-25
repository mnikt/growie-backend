from django.views.generic import ListView, CreateView, DetailView, UpdateView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from gamification.models import Challenge
from gamification.serializers import ChallengeSerializer


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
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer


class ChallengesDetailsApiView(RetrieveAPIView):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer


class ChallengesJoinApiView(APIView):
    def post(self, request, pk):
        try:
            challenge = Challenge.objects.get(pk=pk)
        except Challenge.DoesNotExist:
            return Response(status=404)

        challenge.joined = True
        challenge.save()

        return Response(status=200)


class ChallengesCompleteApiView(APIView):
    def post(self, request, pk):
        try:
            challenge = Challenge.objects.get(pk=pk)
        except Challenge.DoesNotExist:
            return Response(status=404)

        challenge.completed = True
        challenge.save()

        return Response(status=200)