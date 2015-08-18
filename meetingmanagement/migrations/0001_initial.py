# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Acta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_acta', models.DateTimeField(verbose_name=b'Fecha')),
                ('resumen_acta', models.TextField(verbose_name=b'Resumen del Acta')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Elemento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo_elemento', models.CharField(max_length=10, verbose_name=b'Tipo Elemento', choices=[(b'Compromiso', b'Compromiso'), (b'Acuerdo', b'Acuerdo'), (b'Desacuerdo', b'Desacuerdo'), (b'Duda', b'Duda')])),
                ('fecha_inicio', models.DateField(null=True, verbose_name=b'Fecha inicio', blank=True)),
                ('fecha_termino', models.DateField(null=True, verbose_name=b'Fecha termino', blank=True)),
                ('estado_elemento', models.CharField(max_length=20, verbose_name=b'Estado')),
                ('elemento_padre', models.ForeignKey(verbose_name=b'elemento padre', blank=True, to='meetingmanagement.Elemento', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre_proyecto', models.CharField(max_length=50, verbose_name=b'Nombre Proyecto')),
                ('descripcion_proyecto', models.TextField(max_length=600, verbose_name=b'Descripci\xc3\xb3n')),
                ('fecha_inicio_proyecto', models.DateField(null=True, verbose_name=b'Fecha Inicio', blank=True)),
                ('fecha_fin_proyecto', models.DateField(null=True, verbose_name=b'Fecha Finalizaci\xc3\xb3n', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tema',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo_tema', models.CharField(max_length=50)),
                ('descripcion_tema', models.TextField(max_length=600, verbose_name=b'Descripci\xc3\xb3n del Tema')),
                ('acta_tema', models.ForeignKey(related_name=b'acta_tema', verbose_name=b'acta del tema', to='meetingmanagement.Acta')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Usuario_Acta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('presente', models.BooleanField(default=False, verbose_name=b'\xc2\xbfAsisti\xc3\xb3?', choices=[(True, b'S\xc3\xad'), (False, b'No')])),
                ('secretario', models.BooleanField(default=False)),
                ('acta', models.ForeignKey(verbose_name=b'acta', to='meetingmanagement.Acta')),
                ('usuario', models.ForeignKey(verbose_name=b'usuarios participantes', to='meetingmanagement.Usuario')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Usuario_Proyecto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rol_proyecto', models.CharField(max_length=30, verbose_name=b'Rol en el Proyecto', choices=[(b'Miembro Regular', b'Miembro Regular'), (b'Secretario', b'Secretario'), (b'Jefe', b'Jefe')])),
                ('proyecto', models.ForeignKey(verbose_name=b'usuario del proyecto', to='meetingmanagement.Proyecto')),
                ('usuario', models.ForeignKey(verbose_name=b'usuario del proyecto', to='meetingmanagement.Usuario')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='elemento',
            name='tema',
            field=models.ForeignKey(verbose_name=b'tema al que pertenece', to='meetingmanagement.Tema'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='elemento',
            name='usuario_responsable',
            field=models.ForeignKey(verbose_name=b'usuario responsable', blank=True, to='meetingmanagement.Usuario', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='acta',
            name='proyecto_acta',
            field=models.ForeignKey(verbose_name=b'proyecto del acta', to='meetingmanagement.Proyecto'),
            preserve_default=True,
        ),
    ]
