# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetingmanagement', '0009_auto_20150723_1409'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tarea_Kanban',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre_tarea', models.CharField(max_length=50)),
                ('fecha_inicio_tarea', models.DateField(null=True, blank=True)),
                ('fecha_vencimiento_tarea', models.DateField(null=True, blank=True)),
                ('descripcion_tarea', models.CharField(max_length=600, null=True, blank=True)),
                ('elemento_dialogico', models.ForeignKey(to='meetingmanagement.Elemento', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Usuario_Tarea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tarea', models.ForeignKey(to='meetingmanagement.Tarea_Kanban')),
                ('usuario', models.ForeignKey(to='meetingmanagement.Usuario')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='tema',
            name='acta_tema',
            field=models.ForeignKey(verbose_name=b'acta del tema', to='meetingmanagement.Acta'),
        ),
    ]
