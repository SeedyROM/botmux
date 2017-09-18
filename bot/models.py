"""The Bot django data model.
"""
import json
import time

import requests
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import Signal, receiver
from django.utils import timezone
from django_rq import job as queue_job
from TwitterAPI import TwitterAPI

from botmux import settings
from core.models import UUIDModel

from .exceptions import TwitterAccountNotValid


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


# TwitterAccount signals
account_processed = Signal(providing_args=['account'])


# TwitterAccount listeners
@receiver(pre_save, sender=TwitterAccount)
def twitter_account_pre_save(sender, **kwargs):
    """Makes sure our twitter account is valid and starts the listener job.
    """

    profile_page_response = requests.get(
        f'https://twitter.com/{kwargs["instance"].username}'
        )

    if profile_page_response.status_code == 404:
        raise TwitterAccountNotValid


@queue_job
def start_twitter_data_job(account_id):
    print('I\'m starting to run!')

    account = TwitterAccount.objects.get(id=account_id)

    api = TwitterAPI(
        settings.TWITTER_CONSUMER_KEY,
        settings.TWITTER_CONSUMER_SECRET,
        settings.TWITTER_ACCESS_TOKEN_KEY,
        settings.TWITTER_ACCESS_TOKEN_SECRET
        )
    
    timeline_data = api.request(
        'statuses/user_timeline',
        {
            'screen_name': account.username,
            'include_rts': 'false',
            'trim_user': 'true',
            'exclude_replies': 'true',
            'count': 30  # Will be 3200
        }
        )
    tweets = json.loads(timeline_data.text)

    text_to_be_parsed = [tweet['text'] for tweet in tweets]

    account_processed.send(sender=TwitterAccount, account=account)


@receiver(post_save, sender=TwitterAccount)
def twitter_account_post_save(sender, **kwargs):
    if kwargs['created']:
        start_twitter_data_job.delay(account_id=kwargs['instance'].id)


@receiver(account_processed, sender=TwitterAccount)
def twitter_account_finished_processing(sender, account, **kwargs):
    print('Hey this worked!')
    print(account.username)


class TwitterAccountCorpus(UUIDModel):
    """Where the NLP data from each twitter account is stored.
    This will be optimized later to allow for multiple corpuses
    to be retrieved at once.
    """

    twitter_account = models.ForeignKey('bot.TwitterAccount')
