# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetingmanagement', '0002_checklist_kanban_tarea_kanban_usuario_tarea'),
    ]

    operations = [
        migrations.AddField(
            model_name='elemento',
            name='titulo_elemento',
            field=models.CharField(default='qwerty', max_length=50, verbose_name=b'Titulo'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usuario_acta',
            name='presente',
            field=models.BooleanField(default=False, verbose_name=b'\xc2\xbfAsisti\xc3\xb3?'),
        ),
    ]
