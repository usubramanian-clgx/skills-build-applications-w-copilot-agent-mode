from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True, source='_id')
    name = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    team_id = serializers.CharField(max_length=200, required=False, allow_null=True)
    points = serializers.IntegerField(default=0)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if '_id' in instance:
            data['id'] = str(instance['_id'])
        return data

class TeamSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True, source='_id')
    name = serializers.CharField(max_length=200)
    description = serializers.CharField(required=False, allow_blank=True)
    total_points = serializers.IntegerField(default=0)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if '_id' in instance:
            data['id'] = str(instance['_id'])
        return data

class ActivitySerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True, source='_id')
    user_id = serializers.CharField(max_length=200)
    activity_type = serializers.CharField(max_length=100)
    duration = serializers.IntegerField()
    distance = serializers.FloatField(required=False, allow_null=True)
    calories = serializers.IntegerField(required=False, allow_null=True)
    points = serializers.IntegerField(default=0)
    date = serializers.DateTimeField()
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if '_id' in instance:
            data['id'] = str(instance['_id'])
        return data

class LeaderboardSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True, source='_id')
    user_id = serializers.CharField(max_length=200)
    user_name = serializers.CharField(max_length=200)
    team_id = serializers.CharField(max_length=200, required=False, allow_null=True)
    team_name = serializers.CharField(max_length=200, required=False, allow_blank=True)
    total_points = serializers.IntegerField(default=0)
    rank = serializers.IntegerField(required=False, allow_null=True)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if '_id' in instance:
            data['id'] = str(instance['_id'])
        return data

class WorkoutSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True, source='_id')
    user_id = serializers.CharField(max_length=200)
    workout_name = serializers.CharField(max_length=200)
    description = serializers.CharField(required=False, allow_blank=True)
    difficulty_level = serializers.CharField(max_length=50)
    suggested_duration = serializers.IntegerField()
    target_calories = serializers.IntegerField(required=False, allow_null=True)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if '_id' in instance:
            data['id'] = str(instance['_id'])
        return data
