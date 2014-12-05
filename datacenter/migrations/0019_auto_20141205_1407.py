# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('datacenter', '0018_sensor_data_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserWithExtraMethods',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('auth.user',),
        ),
        migrations.AlterModelOptions(
            name='sensordata',
            options={'ordering': ['created_at']},
        ),
    ]
