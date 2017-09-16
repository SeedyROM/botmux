""" Bot manager data model.
"""
from django.db import models
from django.utils import timezone

from core.models import UUIDModel


BOT_MANAGER_FAILED = 0
BOT_MANAGER_STOPPED = 1
BOT_MANAGER_RUNNING = 2

BOT_PROCESS_ERROR = True
BOT_PROCESS_OKAY = True


BOT_MANAGER_STATES = (
    (BOT_MANAGER_FAILED, 'Failed'),
    (BOT_MANAGER_STOPPED, 'Stopped'),
    (BOT_MANAGER_RUNNING, 'Running'),
)


class BotManager(UUIDModel):
    """A model to store the state of bot managers.
    """

    pid = models.BigIntegerField()
    last_status = models.PositiveSmallIntegerField(
        default=BOT_MANAGER_STOPPED,
        choices=BOT_MANAGER_STATES
        )
    last_status_datetime = models.DateTimeField(blank=True, null=True)

    @property
    def time_since_last_active(self):
        """Get time since last status of the manager.
        """
        if self.last_status_datetime:
            return timezone.now() - self.last_state_datetime

        return timezone.ZERO
