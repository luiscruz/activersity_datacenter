# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0003_activitylog'),
    ]

    operations = [
        migrations.AddField(
            model_name='activitylog',
            name='user',
            field=models.ForeignKey(default=1, to='datacenter.User'),
            preserve_default=False,
        ),
    ]
