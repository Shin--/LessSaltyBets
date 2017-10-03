from django.core.management.base import BaseCommand, CommandError
from ...models import Character, SaltyMatch
import requests
import time
from django.db.models import Q


class Command(BaseCommand):
    help = 'Collects salt'

    def add_arguments(self, parser):
        pass
        # parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        characters = Character.objects.all()
        for character in characters:
            losses = character.loser.all()
            wins = character.winner.all()
            if wins or losses:
                character.winrate = 100*(float(len(wins))/(len(losses)+len(wins)))
                character.losses = len(losses)
                character.wins = len(wins)
                character.save()