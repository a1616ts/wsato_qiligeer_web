# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Domains',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='名前', max_length=45)),
                ('display_name', models.CharField(verbose_name='表示名', max_length=255)),
                ('user_id', models.IntegerField(verbose_name='ユーザ')),
                ('server_id', models.IntegerField(verbose_name='ユーザ')),
                ('size', models.IntegerField(verbose_name='ユーザ')),
                ('status', models.CharField(verbose_name='名前', max_length=45)),
                ('create_date', models.DateField()),
                ('update_date', models.DateField()),
            ],
            options={
                'db_table': 'domains',
            },
        ),
    ]
