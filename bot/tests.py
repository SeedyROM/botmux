import glob
import os

from django.test import TestCase
from django_rq import get_worker

from botmux import settings

from .models import TwitterAccount
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

    def tearDown(self):
        chain_files = glob.glob(f'{settings.MEDIA_ROOT}/*.chain')
        for chain_file in chain_files:
            os.remove(chain_file)
        
