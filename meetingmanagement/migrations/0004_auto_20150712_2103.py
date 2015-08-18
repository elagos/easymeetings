# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetingmanagement', '0003_auto_20150712_2052'),
    ]

    operations = [
        migrations.AddField(
            model_name='elemento',
            name='descripcion_elemento',
            field=models.CharField(default='descripcion por defecto', max_length=600, verbose_name=b'Titulo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tarea_kanban',
            name='fecha_inicio_tarea',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
