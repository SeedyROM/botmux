from django.db import models

from django_smalluuid.models import SmallUUIDField, uuid_typed_default


class UUIDModel(models.Model):
    """Abstarct model to create unsequential indentifiers.
    """

    # pylint: disable=C0103
    id = SmallUUIDField(
        default=uuid_typed_default(type=42),
        editable=False,
        primary_key=True
        )

    class Meta:
        abstract = True
