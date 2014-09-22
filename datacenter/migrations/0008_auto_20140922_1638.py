# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0007_auto_20140922_1637'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activitylog',
            name='user',
        ),
        migrations.DeleteModel(
            name='ActivityLog',
        ),
    ]
