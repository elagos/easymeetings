# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('meetingmanagement', '0007_remove_elemento_fecha_asignado'),
    ]

    operations = [
        migrations.AddField(
            model_name='elemento',
            name='fecha_asignado',
            field=models.DateField(default=django.utils.timezone.now, verbose_name=b'Fecha asignado'),
            preserve_default=True,
        ),
    ]
