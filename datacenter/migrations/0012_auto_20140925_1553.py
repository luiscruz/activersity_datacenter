# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0011_remove_sensor_data_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensordata',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
