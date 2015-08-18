# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetingmanagement', '0004_auto_20150712_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='elemento',
            name='estado_elemento',
            field=models.CharField(max_length=50, verbose_name=b'Estado'),
        ),
    ]
