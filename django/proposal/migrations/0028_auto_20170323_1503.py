# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-23 15:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proposal', '0027_auto_20170323_1500'),
    ]

    operations = [
        migrations.RenameField(
            model_name='partner',
            old_name='other_direct_cost',
            new_name='_other_direct_cost',
        ),
    ]
