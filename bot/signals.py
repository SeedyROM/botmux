import json
import os
import zlib
import re

import markovify
import requests

from bot.signals import *
from botmux import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import Signal, receiver
from django_rq import job as queue_job
from TwitterAPI import TwitterAPI

from .exceptions import TwitterAccountNotValid
from .models import MarkovChain, TwitterAccount

# TwitterAccount signals
account_processed = Signal(providing_args=['account'])
account_markov_complete = Signal(providing_args=['account'])


# TwitterAccount listeners
@receiver(pre_save, sender=TwitterAccount)
def twitter_account_pre_save(sender, instance, **kwargs):
    """Makes sure our twitter account is valid and starts the listener job.
    """
    # Make sure this only happens when a record is added to the database.
    if not instance._state.adding: 
        return

    profile_page_response = requests.get(
        f'https://twitter.com/{instance.username}'
        )

    if profile_page_response.status_code == 404:
        raise TwitterAccountNotValid


@receiver(post_save, sender=TwitterAccount)
def twitter_account_post_save(sender, instance, **kwargs):
    if kwargs['created']:
        start_twitter_data_job.delay(account_id=instance.id)


@receiver(account_processed, sender=TwitterAccount)
def twitter_account_finished_processing(sender, account, **kwargs):
    pass


@queue_job
def confirm_markov_created(account):
    pass
    account.save()


# Jobs

@queue_job
def create_chain_file(account, text):
    text_model = markovify.NewlineText(text)

    chain_file_path = os.path.join(
        settings.MEDIA_ROOT,
        f'{account.id}.chain'
        )

    os.makedirs(os.path.dirname(chain_file_path), exist_ok=True)
    with open(chain_file_path, 'wb') as f:
        f.write(zlib.compress(text_model.to_json().encode()))

    account.markov_chain = MarkovChain.objects.create(
        json_file=chain_file_path
        )

    confirm_markov_created.delay(account)
    account_markov_complete.send(sender=TwitterAccount, account=account)

@queue_job
def start_twitter_data_job(account_id):
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
            'count': 1000  # Will be 3200
        }
        )
    tweets = json.loads(timeline_data.text)

    text_to_be_parsed = '\n'.join([tweet['text'] for tweet in tweets])
    text_to_be_parsed = re.sub(r'http\S+', '', text_to_be_parsed)
    text_to_be_parsed = re.sub(r'@\S+', '', text_to_be_parsed)

    create_chain_file.delay(account=account, text=text_to_be_parsed)

    account_processed.send(sender=TwitterAccount, account=account)
