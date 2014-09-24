# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0009_auto_20140922_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='device_type',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='display_name',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
