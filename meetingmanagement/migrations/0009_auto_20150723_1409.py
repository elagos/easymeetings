# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetingmanagement', '0008_elemento_fecha_asignado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tarea_kanban',
            name='checklist_tarea',
        ),
        migrations.DeleteModel(
            name='Checklist_Kanban',
        ),
        migrations.RemoveField(
            model_name='tarea_kanban',
            name='elemento_dialogico',
        ),
        migrations.RemoveField(
            model_name='usuario_tarea',
            name='tarea',
        ),
        migrations.DeleteModel(
            name='Tarea_Kanban',
        ),
        migrations.RemoveField(
            model_name='usuario_tarea',
            name='usuario',
        ),
        migrations.DeleteModel(
            name='Usuario_Tarea',
        ),
        migrations.AlterField(
            model_name='elemento',
            name='descripcion_elemento',
            field=models.CharField(max_length=600, verbose_name=b'Descripcion'),
        ),
    ]
