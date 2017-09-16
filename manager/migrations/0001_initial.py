# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-16 12:30
from __future__ import unicode_literals

from django.db import migrations, models
import django_smalluuid.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BotManager',
            fields=[
                ('id', django_smalluuid.models.SmallUUIDField(default=django_smalluuid.models.UUIDTypedDefault(type=42), editable=False, primary_key=True, serialize=False, unique=True)),
                ('pid', models.BigIntegerField()),
                ('last_status', models.PositiveSmallIntegerField(choices=[(0, 'Failed'), (1, 'Stopped'), (2, 'Running')], default=1)),
                ('last_status_datetime', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
