"""The Bot django data model.
"""
from django.db import models
from django.utils import timezone

from core.models import UUIDModel


class Bot(UUIDModel):
    """Bot data encapsulation.
    """
    # TODO:
    # * Allow for bot protocol definition.
    # * Corpus relation.

    name = models.CharField(max_length=128)


class TwitterAccount(UUIDModel):
    """Twitter reference account.
    """

    bot = models.ForeignKey('bot.Bot', related_name='account')

    username = models.CharField(max_length=64)
    last_post_datetime = models.DateTimeField(blank=True, null=True)

    @property
    def time_since_last_post(self):
        """Retrieve the datetime since last tweet.
        """
        if self.last_post_datetime:
            return timezone.now() - self.last_post_timestamp

        return timezone.ZERO
