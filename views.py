from django.shortcuts import render

from django.views.generic import *
from .models import Character, SaltyMatch
from django.utils import timezone
from django.core.exceptions import ImproperlyConfigured


class OverView(ListView):
    template_name = 'less_salty_bets/overview.html'
    model = Character