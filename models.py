from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

import uuid
# Create your models here.


def get_match_number():
    match_number = SaltyMatch.objects.all()
    if match_number:
        match_number = match_number.latest('match_number')
        return match_number.match_number+1
    return 0


class SaltyBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Character(SaltyBaseModel):
    name = models.CharField(max_length=100)
    winrate = models.FloatField(null=True)
    wins = models.IntegerField(null=True)
    losses = models.IntegerField(null=True)


class SaltyMatch(SaltyBaseModel):
    # characters = models.ManyToManyField(Character, related_name="characters")
    character1 = models.ForeignKey(Character, null=True, related_name="character1")
    character2 = models.ForeignKey(Character, null=True, related_name="character2")
    loser = models.ForeignKey(Character, null=True, related_name="loser")
    winner = models.ForeignKey(Character, null=True, related_name="winner")
    status = models.CharField(max_length=20, null=True)
    match_number = models.IntegerField(default=get_match_number)


@receiver(post_save, sender=SaltyMatch, dispatch_uid="update_character_winrate")
def update_stock(sender, instance, **kwargs):
    if instance.loser and instance.winner:
        for character in [instance.winner, instance.loser]:
            losses = character.loser.all()
            wins = character.winner.all()
            if wins or losses:
                character.winrate = 100 * (float(len(wins)) / (len(losses) + len(wins)))
                character.losses = len(losses)
                character.wins = len(wins)
                character.save()