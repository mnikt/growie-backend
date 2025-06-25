from django.urls import path
from . import views

urlpatterns = [
    path('challenges', views.ChallengesListView.as_view(), name='challenges'),
    path('challenges/form', views.ChallengesCreateView.as_view(), name='challenges_form'),
    path('challenges/details/<int:pk>', views.ChallengesDetailsView.as_view(), name='challenges_details'),
    path('challenges/update/<int:pk>', views.ChallengesUpdateView.as_view(), name='challenges_update'),
    path('challenges/api', views.ChallengesListApiView.as_view(), name='challenges_api_list'),
    path('challenges/api/<int:pk>', views.ChallengesDetailsApiView.as_view(), name='challenges_api_details'),
    path('challenges/api/<int:pk>/join', views.ChallengesJoinApiView.as_view(), name='challenges_api_join'),
    path('challenges/api/<int:pk>/complete', views.ChallengesCompleteApiView.as_view(), name='challenges_api_complete'),
]
