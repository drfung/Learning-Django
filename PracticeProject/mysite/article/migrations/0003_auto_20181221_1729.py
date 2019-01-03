# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-21 09:29
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_auto_20181221_1638'),
    ]

    operations = [
        migrations.RenameField(
            model_name='articlepost',
            old_name='user',
            new_name='author',
        ),
        migrations.AlterField(
            model_name='articlepost',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 21, 9, 29, 33, 589688, tzinfo=utc)),
        ),
    ]