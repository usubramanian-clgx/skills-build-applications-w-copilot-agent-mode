import os
import django
import random
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'octofit_tracker.settings')
django.setup()

from octofit_tracker.api.models import User, Team, Activity, Workout, Leaderboard

# Create Users
def create_users():
    users = []
    for i in range(5):
        user, _ = User.objects.get_or_create(
            username=f'user{i+1}',
            email=f'user{i+1}@example.com',
            first_name=f'First{i+1}',
            last_name=f'Last{i+1}',
        )
        users.append(user)
    return users

# Create Teams
def create_teams(users):
    teams = []
    for i in range(2):
        team, _ = Team.objects.get_or_create(name=f'Team{i+1}')
        for user in users[i*2:(i+1)*2+1]:
            team.members.add(user)
        teams.append(team)
    return teams

# Create Workouts
def create_workouts():
    workouts = []
    for name, diff in [('Pushups', 'Easy'), ('Squats', 'Medium'), ('Burpees', 'Hard')]:
        workout, _ = Workout.objects.get_or_create(name=name, difficulty=diff)
        workouts.append(workout)
    return workouts

# Create Activities
def create_activities(users):
    for user in users:
        for i in range(3):
            Activity.objects.get_or_create(
                user=user,
                activity_type=random.choice(['run', 'cycle', 'swim']),
                duration=random.randint(20, 60),
                calories_burned=random.uniform(100, 500),
                date=date.today() - timedelta(days=i)
            )

# Create Leaderboard
def create_leaderboard(teams):
    for i, team in enumerate(teams):
        Leaderboard.objects.get_or_create(
            team=team,
            total_points=random.randint(100, 500),
            rank=i+1
        )

def main():
    users = create_users()
    teams = create_teams(users)
    create_workouts()
    create_activities(users)
    create_leaderboard(teams)
    print('Test data populated!')

if __name__ == '__main__':
    main()
