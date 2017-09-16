"""Core module's models and classes.
"""


from django.db import models
from django_smalluuid.models import SmallUUIDField, uuid_default

class UUIDModel(models.Model):
    """Abstarct model to create unsequential indentifiers.
    """

    # pylint: disable=C0103
    id = SmallUUIDField(default=uuid_default())

    class Meta:
        abstract = True
