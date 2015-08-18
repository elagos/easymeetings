# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetingmanagement', '0006_elemento_fecha_asignado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='elemento',
            name='fecha_asignado',
        ),
    ]
