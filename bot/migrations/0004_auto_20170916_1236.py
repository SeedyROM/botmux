# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-16 12:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0003_auto_20170916_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twitteraccount',
            name='bots',
            field=models.ManyToManyField(related_name='accounts', to='bot.Bot'),
        ),
    ]
