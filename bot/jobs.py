import os
import json
import zlib

import markovify
from django_rq import job as queue_job
from TwitterAPI import TwitterAPI

from botmux import settings

from .models import TwitterAccount, MarkovChain
from bot.signals import *


@queue_job
def create_chain_file(account, text):
    print('Creating markov chains...')
    text_model = markovify.NewlineText(text)

    chain_file_path = os.path.join(
        settings.MEDIA_ROOT,
        f'{account.id}.chain'
        )

    os.makedirs(os.path.dirname(chain_file_path), exist_ok=True)
    with open(chain_file_path, 'wb') as f:
        f.write(zlib.compress(text_model.to_json().encode()))

    MarkovChain.objects.create(
        twitter_account=account,
        json_file=chain_file_path
        )


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

    text_to_be_parsed = '\n'.join([tweet['text'] for tweet in tweets])

    create_chain_file.delay(account=account, text=text_to_be_parsed)

    account_processed.send(sender=TwitterAccount, account=account)
