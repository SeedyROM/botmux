import requests
import zlib
import markovify

from django.db.models.signals import post_save, pre_save
from django.dispatch import Signal, receiver

from .models import TwitterAccount
from .exceptions import TwitterAccountNotValid
from .jobs import start_twitter_data_job


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
        jobs.start_twitter_data_job.delay(account_id=instance.id)


@receiver(account_processed, sender=TwitterAccount)
def twitter_account_finished_processing(sender, account, **kwargs):
    print('Processed account...')

@receiver(account_markov_complete, sender=TwitterAccount)
def get_a_sentence(sender, account, **kwargs):
    chain_json = json.loads(zlib.decompress(account.markov_chain.read()))
    uncompressed_chain = markovify.Text(chain_json)
    print('Here\'s a sentence: ', uncompressed_chain.make_sentence())
