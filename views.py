from django.shortcuts import render

from django.views.generic import *
from .models import Character, SaltyMatch
from django.utils import timezone
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q


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

    def get_context_data(self, **kwargs):
        context = super(OverView, self).get_context_data(**kwargs)
        context['active_match'] = SaltyMatch.objects.filter(~Q(status='finished') &
                                                            ~Q(status='INVALID'))
        if context['active_match']:
            context['active_match'] = context['active_match'].latest('created_at')
        return context

    def get_queryset(self):
        return super(OverView, self).get_queryset()[:50]


