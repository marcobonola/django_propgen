# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-19 17:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposal', '0023_auto_20170319_1729'),
    ]

    operations = [
        migrations.AddField(
            model_name='partnertype',
            name='description',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
    ]
