from django.core.management.base import BaseCommand
from octofit_tracker.api import models

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Delete existing data
        models.Leaderboard.objects.all().delete()
        models.Activity.objects.all().delete()
        models.Workout.objects.all().delete()
        models.Team.objects.all().delete()
        models.User.objects.all().delete()

        # Create Teams
        marvel = models.Team.objects.create(name='Marvel')
        dc = models.Team.objects.create(name='DC')

        # Create Users
        tony = models.User.objects.create(username='tony', email='tony@marvel.com', first_name='Tony', last_name='Stark')
        steve = models.User.objects.create(username='steve', email='steve@marvel.com', first_name='Steve', last_name='Rogers')
        bruce = models.User.objects.create(username='bruce', email='bruce@dc.com', first_name='Bruce', last_name='Wayne')
        clark = models.User.objects.create(username='clark', email='clark@dc.com', first_name='Clark', last_name='Kent')

        # Add users to teams
        marvel.members.add(tony)
        marvel.members.add(steve)
        dc.members.add(bruce)
        dc.members.add(clark)

        # Create Activities
        from datetime import date
        models.Activity.objects.create(user=tony, activity_type='Run', duration=30, calories_burned=300, date=date.today())
        models.Activity.objects.create(user=steve, activity_type='Swim', duration=45, calories_burned=400, date=date.today())
        models.Activity.objects.create(user=bruce, activity_type='Bike', duration=60, calories_burned=500, date=date.today())
        models.Activity.objects.create(user=clark, activity_type='Yoga', duration=20, calories_burned=150, date=date.today())

        # Create Workouts
        models.Workout.objects.create(name='Avenger HIIT', description='High intensity interval training for Avengers', difficulty='Hard')
        models.Workout.objects.create(name='Justice League Cardio', description='Cardio for Justice League', difficulty='Medium')

        # Create Leaderboard
        models.Leaderboard.objects.create(team=marvel, total_points=1900, rank=1)
        models.Leaderboard.objects.create(team=dc, total_points=1930, rank=2)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
