"""The Bot django data model.
"""
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.dispatch import receiver

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

    @property
    def time_since_last_post(self):
        """Retrieve the datetime since last tweet.
        """
        if self.last_post_datetime:
            return timezone.now() - self.last_post_timestamp

        return timezone.ZERO


@receiver(pre_save, sender=TwitterAccount)
def handle_twitter_account_create(sender, **kwargs):
    """Makes sure our twitter account is valid and starts the listener job.
    """
    print('\n\nWorking on doing twitter things.\n\n')


class TwitterAccountCorpus(UUIDModel):
    """Where the NLP data from each twitter account is stored.
    This will be optimized later to allow for multiple corpuses
    to be retrieved at once.
    """
