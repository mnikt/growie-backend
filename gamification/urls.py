from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('challenges', views.ChallengesListView.as_view(), name='challenges'),
    path('challenges/form', views.ChallengesCreateView.as_view(), name='challenges_form'),
    path('challenges/details/<int:pk>', views.ChallengesDetailsView.as_view(), name='challenges_details'),
    path('challenges/update/<int:pk>', views.ChallengesUpdateView.as_view(), name='challenges_update'),
    path('challenges/api', views.ChallengesListApiView.as_view(), name='challenges_api_list'),
    path('challenges/api/<int:pk>', views.ChallengesDetailsApiView.as_view(), name='challenges_api_details'),
    path('challenges/api/<int:pk>/join', views.ChallengesJoinApiView.as_view(), name='challenges_api_join'),
    path('challenges/api/<int:pk>/claim', views.ChallengesCompleteApiView.as_view(), name='challenges_api_claim'),
    path('points/api', views.PointsApiView.as_view(), name='points_api_get'),
    path('events', views.EventListView.as_view(), name='events'),
    path('events/form', views.EventCreateView.as_view(), name='events_form'),
    path('events/details/<int:pk>', views.EventsDetailsView.as_view(), name='events_details'),
    path('events/update/<int:pk>', views.EventsUpdateView.as_view(), name='events_update'),
    path('quizzes', views.QuizListView.as_view(), name='quizzes'),
    path('quizzes/form', views.QuizCreateView.as_view(), name='quizzes_form'),
    path('quizzes/details/<int:pk>', views.QuizDetailsView.as_view(), name='quizzes_details'),
    path('quizzes/update/<int:pk>', views.QuizUpdateView.as_view(), name='quizzes_update')
]

