# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('meetingmanagement', '0005_auto_20150721_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='elemento',
            name='fecha_asignado',
            field=models.DateField(default=django.utils.timezone.now, null=True, verbose_name=b'Fecha asignado', blank=True),
            preserve_default=True,
        ),
    ]
