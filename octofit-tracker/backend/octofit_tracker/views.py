from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId
from .models import get_mongo_db, USERS_COLLECTION, TEAMS_COLLECTION, ACTIVITIES_COLLECTION, LEADERBOARD_COLLECTION, WORKOUTS_COLLECTION
from .serializers import UserSerializer, TeamSerializer, ActivitySerializer, LeaderboardSerializer, WorkoutSerializer

@api_view(['GET'])
def api_root(request):
    """
    API root endpoint
    """
    import os
    codespace_name = os.environ.get('CODESPACE_NAME')
    if codespace_name:
        base_url = f"https://{codespace_name}-8000.app.github.dev"
    else:
        base_url = "http://localhost:8000"
    
    return Response({
        'users': f'{base_url}/api/users/',
        'teams': f'{base_url}/api/teams/',
        'activities': f'{base_url}/api/activities/',
        'leaderboard': f'{base_url}/api/leaderboard/',
        'workouts': f'{base_url}/api/workouts/',
    })

# User views
@api_view(['GET', 'POST'])
def user_list(request):
    db = get_mongo_db()
    
    if request.method == 'GET':
        users = list(db[USERS_COLLECTION].find())
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            result = db[USERS_COLLECTION].insert_one(serializer.validated_data)
            user = db[USERS_COLLECTION].find_one({'_id': result.inserted_id})
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    db = get_mongo_db()
    
    try:
        user = db[USERS_COLLECTION].find_one({'_id': ObjectId(pk)})
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            db[USERS_COLLECTION].update_one(
                {'_id': ObjectId(pk)},
                {'$set': serializer.validated_data}
            )
            user = db[USERS_COLLECTION].find_one({'_id': ObjectId(pk)})
            return Response(UserSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        db[USERS_COLLECTION].delete_one({'_id': ObjectId(pk)})
        return Response(status=status.HTTP_204_NO_CONTENT)

# Team views
@api_view(['GET', 'POST'])
def team_list(request):
    db = get_mongo_db()
    
    if request.method == 'GET':
        teams = list(db[TEAMS_COLLECTION].find())
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            result = db[TEAMS_COLLECTION].insert_one(serializer.validated_data)
            team = db[TEAMS_COLLECTION].find_one({'_id': result.inserted_id})
            return Response(TeamSerializer(team).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def team_detail(request, pk):
    db = get_mongo_db()
    
    try:
        team = db[TEAMS_COLLECTION].find_one({'_id': ObjectId(pk)})
        if not team:
            return Response(status=status.HTTP_404_NOT_FOUND)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = TeamSerializer(team)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            db[TEAMS_COLLECTION].update_one(
                {'_id': ObjectId(pk)},
                {'$set': serializer.validated_data}
            )
            team = db[TEAMS_COLLECTION].find_one({'_id': ObjectId(pk)})
            return Response(TeamSerializer(team).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        db[TEAMS_COLLECTION].delete_one({'_id': ObjectId(pk)})
        return Response(status=status.HTTP_204_NO_CONTENT)

# Activity views
@api_view(['GET', 'POST'])
def activity_list(request):
    db = get_mongo_db()
    
    if request.method == 'GET':
        activities = list(db[ACTIVITIES_COLLECTION].find())
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ActivitySerializer(data=request.data)
        if serializer.is_valid():
            result = db[ACTIVITIES_COLLECTION].insert_one(serializer.validated_data)
            activity = db[ACTIVITIES_COLLECTION].find_one({'_id': result.inserted_id})
            return Response(ActivitySerializer(activity).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def activity_detail(request, pk):
    db = get_mongo_db()
    
    try:
        activity = db[ACTIVITIES_COLLECTION].find_one({'_id': ObjectId(pk)})
        if not activity:
            return Response(status=status.HTTP_404_NOT_FOUND)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ActivitySerializer(activity)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ActivitySerializer(data=request.data)
        if serializer.is_valid():
            db[ACTIVITIES_COLLECTION].update_one(
                {'_id': ObjectId(pk)},
                {'$set': serializer.validated_data}
            )
            activity = db[ACTIVITIES_COLLECTION].find_one({'_id': ObjectId(pk)})
            return Response(ActivitySerializer(activity).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        db[ACTIVITIES_COLLECTION].delete_one({'_id': ObjectId(pk)})
        return Response(status=status.HTTP_204_NO_CONTENT)

# Leaderboard views
@api_view(['GET', 'POST'])
def leaderboard_list(request):
    db = get_mongo_db()
    
    if request.method == 'GET':
        leaderboard = list(db[LEADERBOARD_COLLECTION].find().sort('total_points', -1))
        serializer = LeaderboardSerializer(leaderboard, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = LeaderboardSerializer(data=request.data)
        if serializer.is_valid():
            result = db[LEADERBOARD_COLLECTION].insert_one(serializer.validated_data)
            entry = db[LEADERBOARD_COLLECTION].find_one({'_id': result.inserted_id})
            return Response(LeaderboardSerializer(entry).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def leaderboard_detail(request, pk):
    db = get_mongo_db()
    
    try:
        entry = db[LEADERBOARD_COLLECTION].find_one({'_id': ObjectId(pk)})
        if not entry:
            return Response(status=status.HTTP_404_NOT_FOUND)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = LeaderboardSerializer(entry)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = LeaderboardSerializer(data=request.data)
        if serializer.is_valid():
            db[LEADERBOARD_COLLECTION].update_one(
                {'_id': ObjectId(pk)},
                {'$set': serializer.validated_data}
            )
            entry = db[LEADERBOARD_COLLECTION].find_one({'_id': ObjectId(pk)})
            return Response(LeaderboardSerializer(entry).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        db[LEADERBOARD_COLLECTION].delete_one({'_id': ObjectId(pk)})
        return Response(status=status.HTTP_204_NO_CONTENT)

# Workout views
@api_view(['GET', 'POST'])
def workout_list(request):
    db = get_mongo_db()
    
    if request.method == 'GET':
        workouts = list(db[WORKOUTS_COLLECTION].find())
        serializer = WorkoutSerializer(workouts, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = WorkoutSerializer(data=request.data)
        if serializer.is_valid():
            result = db[WORKOUTS_COLLECTION].insert_one(serializer.validated_data)
            workout = db[WORKOUTS_COLLECTION].find_one({'_id': result.inserted_id})
            return Response(WorkoutSerializer(workout).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def workout_detail(request, pk):
    db = get_mongo_db()
    
    try:
        workout = db[WORKOUTS_COLLECTION].find_one({'_id': ObjectId(pk)})
        if not workout:
            return Response(status=status.HTTP_404_NOT_FOUND)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = WorkoutSerializer(workout)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = WorkoutSerializer(data=request.data)
        if serializer.is_valid():
            db[WORKOUTS_COLLECTION].update_one(
                {'_id': ObjectId(pk)},
                {'$set': serializer.validated_data}
            )
            workout = db[WORKOUTS_COLLECTION].find_one({'_id': ObjectId(pk)})
            return Response(WorkoutSerializer(workout).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        db[WORKOUTS_COLLECTION].delete_one({'_id': ObjectId(pk)})
        return Response(status=status.HTTP_204_NO_CONTENT)
