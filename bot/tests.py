import glob
import os

from django.test import TestCase
from django_rq import get_worker

from botmux import settings

from .models import TwitterAccount, MarkovChain
from .exceptions import TwitterAccountNotValid


class TwitterAccountCase(TestCase):
    """ Test the TwitterAccount model.
    """

    def test_account_exists(self):
        with self.assertRaises(TwitterAccountNotValid) as c:
            account = TwitterAccount.objects.create(username=':#--4--x')

    def test_account_data_job(self):
        account = TwitterAccount.objects.create(username='dril')
        try:
            get_worker().work(burst=True)
        except BaseException as e:
            self.fail()

    def test_account_markov_create(self):
        account = TwitterAccount.objects.create(username='dril')

        get_worker().work(burst=True)

        account.refresh_from_db()
        self.assertIsNotNone(account.markov_chain)

        chain_id = account.markov_chain.json_file.url
        chain_id = chain_id.split('.')[0].split('/')[-1]

        self.assertEqual(chain_id, str(account.id))

    def test_generates_sentences(self):
        account = TwitterAccount.objects.create(username='horse_ebooks')

        get_worker().work(burst=True)

        account.refresh_from_db()
        chain = account.get_uncompressed_chain()
        sentence = chain.make_sentence(tries=100)

        import pdb; pdb.set_trace()
        print(sentence)

        self.assertIsNotNone(sentence)

    def tearDown(self):
        chain_files = glob.glob(f'{settings.MEDIA_ROOT}/*.chain')
        for chain_file in chain_files:
            os.remove(chain_file)
