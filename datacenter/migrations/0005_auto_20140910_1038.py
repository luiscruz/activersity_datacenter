# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0004_activitylog_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitylog',
            name='data',
            field=jsonfield.fields.JSONField(),
        ),
    ]
