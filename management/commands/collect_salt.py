from django.core.management.base import BaseCommand, CommandError
from ...models import Character, SaltyMatch
import requests
import time
import sys
from random import randint
from django.db.models import Q

class Command(BaseCommand):
    help = 'Collects salt'
    has_been_opened = False
    has_been_locked = False

    def add_arguments(self, parser):
        pass
        # parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):

        while True:
            request = requests.get('http://www.saltybet.com/state.json')
            state = request.json()

            p1name = state.get('p1name')
            p2name = state.get('p2name')
            p1 = Character.objects.filter(name=p1name)
            if not p1.exists():
                p1 = Character.objects.create(name=p1name)
            else:
                p1 = p1[0]
            p2 = Character.objects.filter(name=p2name)
            if not p2.exists():
                p2 = Character.objects.create(name=p2name)
            else:
                p2 = p2[0]
            match = SaltyMatch.objects.filter(~Q(status='finished') & ~Q(status='INVALID'),
                                                character1__in=[p1, p2],
                                                character2__in=[p1, p2])
            if match.exists():
                sleeping = randint(20, 50) / 10.0
                match = match.latest('match_number')
                if state.get('status') == 'open':
                    sleeping = (sleeping if self.has_been_opened else 20)
                    self.has_been_opened = True
                if state.get('status') == 'locked':
                    sleeping = (sleeping if self.has_been_locked else 30)
                    self.has_been_locked = True
                elif state.get('status') == "1":
                    match.winner = match.character1
                    match.loser = match.character2
                    match.status = 'finished'
                    match.save()
                    print("finished (1)")
                elif state.get('status') == "2":
                    match.winner = match.character2
                    match.loser = match.character1
                    match.status = 'finished'
                    match.save()
                    print("finished (2)")

            elif state.get('status') == '1' or state.get('status') == '2':
                sleeping = 5

            else:
                sleeping = 30
                match = SaltyMatch.objects.create(character1=p1, character2=p2,
                                             status=state.get('status'))
                self.has_been_opened= False
                self.has_been_locked = False
                last_match = SaltyMatch.objects.filter(match_number=match.match_number-1)
                if last_match.exists():
                    last_match = last_match[0]
                    if last_match.status != ('finished' or 'INVALID'):
                        last_match.status = 'INVALID'
                        last_match.save()
                        print("Last match (#%d) set to INVALID" % last_match.match_number)
                print "new match #%d started" % match.match_number

            # print('status: ', state.get('status'))
            # finished_match = SaltyMatch.objects.filter(~Q(status='finished') & ~Q(status='INVALID'), match_number=match.match_number - 1)
            # if finished_match.exists():
            #     finished_match = finished_match[0]
            #     print('status: ', state.get('status'), " SAVE!")
            #     if state.get('status') == "1":
            #         finished_match.winner = finished_match.character1
            #         finished_match.loser = finished_match.character2
            #         finished_match.status = 'finished'
            #     elif state.get('status') == "2":
            #         finished_match.winner = finished_match.character2
            #         finished_match.loser = finished_match.character1
            #         finished_match.status = 'finished'
            #     else:
            #         finished_match.status = 'INVALID'
            #     finished_match.save()

            sys.stdout.flush()
            time.sleep(sleeping)