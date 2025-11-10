from django.db import models
from django.conf import settings
from pymongo import MongoClient

# MongoDB connection helper
def get_mongo_db():
    client = MongoClient(settings.MONGODB_URI)
    return client[settings.MONGODB_NAME]

# Collection names
USERS_COLLECTION = 'users'
TEAMS_COLLECTION = 'teams'
ACTIVITIES_COLLECTION = 'activities'
LEADERBOARD_COLLECTION = 'leaderboard'
WORKOUTS_COLLECTION = 'workouts'
