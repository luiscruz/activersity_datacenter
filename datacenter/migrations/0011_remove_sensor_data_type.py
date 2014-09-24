# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0010_auto_20140924_1023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sensor',
            name='data_type',
        ),
    ]
