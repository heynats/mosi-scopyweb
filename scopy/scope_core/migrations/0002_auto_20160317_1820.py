# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-17 10:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scope_core', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Jobs',
            new_name='Job',
        ),
    ]