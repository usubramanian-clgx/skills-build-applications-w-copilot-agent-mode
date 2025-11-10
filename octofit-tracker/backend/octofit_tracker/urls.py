"""
URL configuration for octofit_tracker project.
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.api_root, name='api-root'),
    path('api/', views.api_root, name='api-root'),
    
    # User endpoints
    path('api/users/', views.user_list, name='user-list'),
    path('api/users/<str:pk>/', views.user_detail, name='user-detail'),
    
    # Team endpoints
    path('api/teams/', views.team_list, name='team-list'),
    path('api/teams/<str:pk>/', views.team_detail, name='team-detail'),
    
    # Activity endpoints
    path('api/activities/', views.activity_list, name='activity-list'),
    path('api/activities/<str:pk>/', views.activity_detail, name='activity-detail'),
    
    # Leaderboard endpoints
    path('api/leaderboard/', views.leaderboard_list, name='leaderboard-list'),
    path('api/leaderboard/<str:pk>/', views.leaderboard_detail, name='leaderboard-detail'),
    
    # Workout endpoints
    path('api/workouts/', views.workout_list, name='workout-list'),
    path('api/workouts/<str:pk>/', views.workout_detail, name='workout-detail'),
]
