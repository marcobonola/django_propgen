# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-02 13:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proposal', '0008_auto_20170302_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='lead',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proposal.Partner', verbose_name='Project coordinator'),
        ),
    ]
