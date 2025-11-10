from django.core.management.base import BaseCommand
from octofit_tracker.models import get_mongo_db, USERS_COLLECTION, TEAMS_COLLECTION, ACTIVITIES_COLLECTION, LEADERBOARD_COLLECTION, WORKOUTS_COLLECTION
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        db = get_mongo_db()
        
        self.stdout.write('Clearing existing data...')
        # Clear existing collections
        db[USERS_COLLECTION].delete_many({})
        db[TEAMS_COLLECTION].delete_many({})
        db[ACTIVITIES_COLLECTION].delete_many({})
        db[LEADERBOARD_COLLECTION].delete_many({})
        db[WORKOUTS_COLLECTION].delete_many({})
        
        # Create unique index on email
        db[USERS_COLLECTION].create_index('email', unique=True)
        
        self.stdout.write('Creating teams...')
        # Create Teams
        teams = [
            {
                'name': 'Team Marvel',
                'description': 'Assemble! The mightiest heroes team',
                'total_points': 0
            },
            {
                'name': 'Team DC',
                'description': 'Justice League united for fitness',
                'total_points': 0
            }
        ]
        team_results = db[TEAMS_COLLECTION].insert_many(teams)
        team_ids = list(team_results.inserted_ids)
        
        self.stdout.write('Creating users...')
        # Create Users (Superheroes)
        users = [
            # Team Marvel
            {'name': 'Iron Man', 'email': 'tony.stark@marvel.com', 'team_id': str(team_ids[0]), 'points': 850},
            {'name': 'Captain America', 'email': 'steve.rogers@marvel.com', 'team_id': str(team_ids[0]), 'points': 920},
            {'name': 'Thor', 'email': 'thor.odinson@marvel.com', 'team_id': str(team_ids[0]), 'points': 780},
            {'name': 'Black Widow', 'email': 'natasha.romanoff@marvel.com', 'team_id': str(team_ids[0]), 'points': 890},
            {'name': 'Hulk', 'email': 'bruce.banner@marvel.com', 'team_id': str(team_ids[0]), 'points': 950},
            {'name': 'Spider-Man', 'email': 'peter.parker@marvel.com', 'team_id': str(team_ids[0]), 'points': 820},
            
            # Team DC
            {'name': 'Superman', 'email': 'clark.kent@dc.com', 'team_id': str(team_ids[1]), 'points': 980},
            {'name': 'Batman', 'email': 'bruce.wayne@dc.com', 'team_id': str(team_ids[1]), 'points': 940},
            {'name': 'Wonder Woman', 'email': 'diana.prince@dc.com', 'team_id': str(team_ids[1]), 'points': 910},
            {'name': 'The Flash', 'email': 'barry.allen@dc.com', 'team_id': str(team_ids[1]), 'points': 1000},
            {'name': 'Aquaman', 'email': 'arthur.curry@dc.com', 'team_id': str(team_ids[1]), 'points': 870},
            {'name': 'Green Lantern', 'email': 'hal.jordan@dc.com', 'team_id': str(team_ids[1]), 'points': 840},
        ]
        user_results = db[USERS_COLLECTION].insert_many(users)
        user_ids = list(user_results.inserted_ids)
        
        # Calculate team points
        marvel_points = sum(u['points'] for u in users[:6])
        dc_points = sum(u['points'] for u in users[6:])
        
        db[TEAMS_COLLECTION].update_one({'_id': team_ids[0]}, {'$set': {'total_points': marvel_points}})
        db[TEAMS_COLLECTION].update_one({'_id': team_ids[1]}, {'$set': {'total_points': dc_points}})
        
        self.stdout.write('Creating activities...')
        # Create Activities
        activity_types = ['Running', 'Walking', 'Cycling', 'Swimming', 'Strength Training', 'Yoga']
        activities = []
        
        for i, user_id in enumerate(user_ids):
            user_email = users[i]['email']
            for _ in range(random.randint(3, 7)):
                activity_type = random.choice(activity_types)
                duration = random.randint(15, 90)
                distance = round(random.uniform(1.0, 15.0), 2) if activity_type in ['Running', 'Walking', 'Cycling'] else None
                calories = random.randint(50, 500)
                points = duration + (calories // 10)
                
                activity = {
                    'user_id': str(user_id),
                    'activity_type': activity_type,
                    'duration': duration,
                    'distance': distance,
                    'calories': calories,
                    'points': points,
                    'date': datetime.now() - timedelta(days=random.randint(0, 30))
                }
                activities.append(activity)
        
        if activities:
            db[ACTIVITIES_COLLECTION].insert_many(activities)
        
        self.stdout.write('Creating leaderboard entries...')
        # Create Leaderboard
        leaderboard_entries = []
        for i, user in enumerate(users):
            team = teams[0] if i < 6 else teams[1]
            entry = {
                'user_id': str(user_ids[i]),
                'user_name': user['name'],
                'team_id': str(team_ids[0] if i < 6 else team_ids[1]),
                'team_name': team['name'],
                'total_points': user['points'],
                'rank': i + 1
            }
            leaderboard_entries.append(entry)
        
        # Sort by points and update ranks
        leaderboard_entries.sort(key=lambda x: x['total_points'], reverse=True)
        for i, entry in enumerate(leaderboard_entries):
            entry['rank'] = i + 1
        
        if leaderboard_entries:
            db[LEADERBOARD_COLLECTION].insert_many(leaderboard_entries)
        
        self.stdout.write('Creating workouts...')
        # Create Workouts
        workouts = [
            {
                'user_id': str(user_ids[0]),
                'workout_name': 'Arc Reactor Cardio',
                'description': 'High-intensity cardio workout',
                'difficulty_level': 'Advanced',
                'suggested_duration': 45,
                'target_calories': 400
            },
            {
                'user_id': str(user_ids[1]),
                'workout_name': 'Super Soldier Training',
                'description': 'Complete body strength training',
                'difficulty_level': 'Advanced',
                'suggested_duration': 60,
                'target_calories': 500
            },
            {
                'user_id': str(user_ids[2]),
                'workout_name': 'Asgardian Power Lift',
                'description': 'Heavy weight lifting routine',
                'difficulty_level': 'Expert',
                'suggested_duration': 50,
                'target_calories': 450
            },
            {
                'user_id': str(user_ids[6]),
                'workout_name': 'Kryptonian Strength',
                'description': 'Maximum power workout',
                'difficulty_level': 'Expert',
                'suggested_duration': 55,
                'target_calories': 550
            },
            {
                'user_id': str(user_ids[9]),
                'workout_name': 'Speed Force Sprint',
                'description': 'Speed and agility training',
                'difficulty_level': 'Advanced',
                'suggested_duration': 40,
                'target_calories': 450
            },
            {
                'user_id': str(user_ids[5]),
                'workout_name': 'Web-Slinger Workout',
                'description': 'Bodyweight and flexibility training',
                'difficulty_level': 'Intermediate',
                'suggested_duration': 35,
                'target_calories': 300
            },
        ]
        db[WORKOUTS_COLLECTION].insert_many(workouts)
        
        self.stdout.write(self.style.SUCCESS('Successfully populated database!'))
        self.stdout.write(f'Created {len(teams)} teams')
        self.stdout.write(f'Created {len(users)} users')
        self.stdout.write(f'Created {len(activities)} activities')
        self.stdout.write(f'Created {len(leaderboard_entries)} leaderboard entries')
        self.stdout.write(f'Created {len(workouts)} workouts')
