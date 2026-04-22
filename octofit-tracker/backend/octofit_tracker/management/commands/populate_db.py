from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models


from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB directly for index creation
        client = MongoClient('mongodb://localhost:27017/')
        db = client['octofit_db']
        db.users.create_index([('email', 1)], unique=True)

        # Clear collections
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Teams
        marvel = {'name': 'Team Marvel'}
        dc = {'name': 'Team DC'}
        marvel_id = db.teams.insert_one(marvel).inserted_id
        dc_id = db.teams.insert_one(dc).inserted_id

        # Users
        users = [
            {'name': 'Superman', 'email': 'superman@dc.com', 'team_id': dc_id},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team_id': dc_id},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team_id': dc_id},
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team_id': marvel_id},
            {'name': 'Captain America', 'email': 'cap@marvel.com', 'team_id': marvel_id},
            {'name': 'Black Widow', 'email': 'widow@marvel.com', 'team_id': marvel_id},
        ]
        user_ids = db.users.insert_many(users).inserted_ids

        # Activities
        activities = [
            {'user_id': user_ids[0], 'activity': 'Flight', 'duration': 60},
            {'user_id': user_ids[1], 'activity': 'Martial Arts', 'duration': 45},
            {'user_id': user_ids[3], 'activity': 'Suit Up', 'duration': 30},
            {'user_id': user_ids[4], 'activity': 'Shield Training', 'duration': 50},
        ]
        db.activities.insert_many(activities)

        # Leaderboard
        leaderboard = [
            {'team_id': marvel_id, 'points': 150},
            {'team_id': dc_id, 'points': 120},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Workouts
        workouts = [
            {'name': 'Strength', 'description': 'Strength training workout'},
            {'name': 'Cardio', 'description': 'Cardio workout'},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
