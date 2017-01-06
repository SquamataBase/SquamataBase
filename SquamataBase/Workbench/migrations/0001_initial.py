# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-23 13:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Workbench',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'sb_workbench',
            },
        ),
        migrations.CreateModel(
            name='FoodRecordWorkbench',
            fields=[
            ],
            options={
                'proxy': True,
                'verbose_name': 'food record',
                'verbose_name_plural': 'food records'
            },
            bases=('Workbench.workbench',),
        ),
    ]
