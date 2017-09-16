from django.db import models

from core.models import UUIDModel


class Bot(UUIDModel):
    """Bot data encapsulation.
    """
    # TODO: 
    # [ ] Allow for bot protocol definition.
    # [ ] Corpus relation.
    name = models.CharField(max_length=128)
