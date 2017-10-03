# -*- coding: utf-8 -*-

import requests
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'great_news.settings'
import django
django.setup()

import websocket
import thread
import time
import json

# from .models import Character, Match


def on_message(ws, message):
    print("message:", message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def run(*args):
        for i in range(3):
            time.sleep(1)
        time.sleep(1)
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    request = requests.get("http://www-cdn-twitch.saltybet.com:1337/socket.io/?EIO=3&transport=polling")
    websocket_data = json.loads('{'+request.content.split('{')[1])

    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://www-cdn-twitch.saltybet.com:1337/socket.io/?EIO=3&transport=websocket&sid=%s" % websocket_data.get('sid'),
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
    #
    # p1name = None
    # p2name = None
    # ongoing_match = False
    # while True:
    #     request = requests.get('http://www.saltybet.com/state.json')
    #     state = request.json()
    #
    #     p1name = state.get('p1name')
    #     p2name = state.get('p2name')
    #     p1 = Character.objects.filter(name=p1name)
    #     if not p1.exists():
    #         p1 = Character.objects.create(name=p1name)
    #     p2 = Character.objects.filter(name=p2name)
    #     if not p2.exists():
    #         p2 = Character.objects.create(name=p2name)
    #
    #     match = Match.objects.filter(character1__in=[p1, p2],
    #                                  character2__in=[p1, p2],
    #                                  status__ne='finished')
    #     if match.exists():
    #         match = match.latest('created_at')
    #         if match.status == state.get('status'):
    #             match.status = state.get('status')
    #     else:
    #         match = Match.objects.create(character1=p1, character=p2,
    #                                     status=state.get('status'))
    #
    #     finished_match = Match.objects.filter(match_number=match.match_number-1, status__ne='finished')
    #     if finished_match.exists():
    #         finished_match = finished_match[0]
    #         if state.get('x') == 0:
    #             finished_match.winner = finished_match.character1
    #             finished_match.loser = finished_match.character2
    #         elif state.get('x') == 1:
    #             finished_match.winner = finished_match.character2
    #             finished_match.loser = finished_match.character1
    #         finished_match.status = 'finished'
    #         finished_match.save()
    #     time.sleep(5)
