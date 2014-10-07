# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0015_auto_20141007_1021'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sensor',
            name='device',
        ),
    ]
