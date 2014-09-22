# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0008_auto_20140922_1638'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sensor',
            name='description',
        ),
        migrations.AddField(
            model_name='sensor',
            name='data_type',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sensor',
            name='device_type',
            field=models.CharField(default='na', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sensor',
            name='display_name',
            field=models.CharField(default='na', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sensor',
            name='name',
            field=models.CharField(default='na', max_length=200),
            preserve_default=False,
        ),
    ]
