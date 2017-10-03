from django.shortcuts import render

from django.views.generic import *
from .models import Character, SaltyMatch
from django.utils import timezone
from django.core.exceptions import ImproperlyConfigured


class OverView(ListView):
    template_name = 'less_salty_bets/player_overview.html'
    model = Character
    ordering = ['-performance']

    def dispatch(self, request, *args, **kwargs):
        if request.GET.get('type') == 'players':
            self.template_name = 'less_salty_bets/player_overview.html'
            self.model = Character
            self.ordering = ['-performance']
        elif request.GET.get('type') == 'matches':
            self.template_name = 'less_salty_bets/match_overview.html'
            self.model = SaltyMatch
            self.ordering = ['-match_number']
        return super(OverView, self).dispatch(request, *args, **kwargs)


