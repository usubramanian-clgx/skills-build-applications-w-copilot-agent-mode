 # Codespace URL pattern: -8000.app.github.dev

import os
from rest_framework import routers
from .views import UserViewSet, TeamViewSet, ActivityViewSet, WorkoutViewSet, LeaderboardViewSet
from django.urls import path, include
from rest_framework.response import Response
from rest_framework.decorators import api_view

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'activities', ActivityViewSet)
router.register(r'workouts', WorkoutViewSet)
router.register(r'leaderboard', LeaderboardViewSet)

@api_view(['GET'])
def api_root(request, format=None):
    codespace_name = os.environ.get('CODESPACE_NAME', None)
    if codespace_name:
        base_url = f"https://{codespace_name}-90.app.github.dev/api/"
    else:
        base_url = request.build_absolute_uri('/')
    return Response({
        'users': base_url + 'users/',
        'teams': base_url + 'teams/',
        'activities': base_url + 'activities/',
        'workouts': base_url + 'workouts/',
        'leaderboard': base_url + 'leaderboard/',
    })

urlpatterns = [
    path('', api_root, name='api-root'),
    path('', include(router.urls)),
]
