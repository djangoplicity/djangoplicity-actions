# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-08-06 00:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('actions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SomeEventAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('on_event', models.CharField(db_index=True, max_length=50)),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='actions.Action')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SomeListTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_key', models.CharField(max_length=255, verbose_name=b'API key')),
                ('list_id', models.CharField(max_length=50, unique=True)),
                ('web_id', models.CharField(blank=True, max_length=255)),
                ('connected', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='someeventaction',
            name='model_object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='test_project.SomeListTest'),
        ),
    ]
