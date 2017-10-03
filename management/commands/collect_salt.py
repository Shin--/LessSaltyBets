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
        p1name = None
        p2name = None
        ongoing_match = False
        while True:
            p1name = None
            p2name = None
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
            match = SaltyMatch.objects.filter(~Q(status='finished'),
                                        character1__in=[p1, p2],
                                        character2__in=[p1, p2])
            if match.exists():
                match = match.latest('created_at')
                if match.status == state.get('status'):
                    match.status = state.get('status')
            else:
                match = SaltyMatch.objects.create(character1=p1, character2=p2,
                                             status=state.get('status'))
                print "new match #%d started" % match.match_number

            finished_match = SaltyMatch.objects.filter(~Q(status='finished'), match_number=match.match_number - 1)
            if finished_match.exists():
                finished_match = finished_match[0]
                if state.get('x') == 0:
                    finished_match.winner = finished_match.character1
                    finished_match.loser = finished_match.character2
                elif state.get('x') == 1:
                    finished_match.winner = finished_match.character2
                    finished_match.loser = finished_match.character1
                finished_match.status = 'finished'
                finished_match.save()
                print "match #%d finished. %s won against %s" % (finished_match.match_number,
                                                                 finished_match.winner.name,
                                                                 finished_match.loser.name)
            time.sleep(15)