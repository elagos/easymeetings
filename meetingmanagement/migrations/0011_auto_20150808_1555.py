# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetingmanagement', '0010_auto_20150807_0215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='elemento',
            name='tema',
            field=models.ForeignKey(verbose_name=b'tema al que pertenece', blank=True, to='meetingmanagement.Tema', null=True),
        ),
    ]
