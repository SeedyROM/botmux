"""The Bot django data model.
"""
import time

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

    bots = models.ManyToManyField('bot.Bot', related_name='accounts')

    username = models.CharField(max_length=64)
    last_post_datetime = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        """Casefold the username when the model
        is saved for the first time.Casefold the username to avoid
        """
        if not self.pk:
            self.username = self.username.casefold()
        
        super(UUIDModel, self).save(*args, **kwargs)

    @property
    def time_since_last_post(self):
        """Retrieve the datetime since last tweet.
        """
        if self.last_post_datetime:
            return timezone.now() - self.last_post_timestamp

        return timezone.ZERO


class MarkovChain(UUIDModel):
    """Where the NLP data from each twitter account is stored.
    This will be optimized later to allow for multiple corpuses
    to be retrieved at once.
    """

    twitter_account = models.ForeignKey('bot.TwitterAccount')
    json_file = models.FileField(upload_to='chains', blank=True, null=True)

    @property
    def has_chain(self):
        return self.markov_chain
