# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0016_remove_sensor_device'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor',
            name='device',
            field=models.ForeignKey(to='datacenter.Device', null=True),
            preserve_default=True,
        ),
    ]
