# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0014_device'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='device_type',
            field=models.CharField(max_length=200),
        ),
    ]
