# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetingmanagement', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Checklist_Kanban',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item', models.CharField(max_length=b'50')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tarea_Kanban',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre_tarea', models.CharField(max_length=50)),
                ('fecha_vencimiento_tarea', models.DateField(null=True, blank=True)),
                ('descripcion_tarea', models.CharField(max_length=600, null=True, blank=True)),
                ('checklist_tarea', models.ForeignKey(blank=True, to='meetingmanagement.Checklist_Kanban', null=True)),
                ('elemento_dialogico', models.ForeignKey(to='meetingmanagement.Elemento')),
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
    ]
