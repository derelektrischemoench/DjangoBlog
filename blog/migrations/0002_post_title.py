# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-14 08:43
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.CharField(default=datetime.datetime(2016, 4, 14, 8, 43, 13, 71781, tzinfo=utc), max_length=250),
            preserve_default=False,
        ),
    ]
