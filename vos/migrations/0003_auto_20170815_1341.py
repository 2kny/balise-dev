# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-15 13:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vos', '0002_auto_20170804_1224'),
    ]

    operations = [
        migrations.RenameField(
            model_name='montantcheque',
            old_name='ordre',
            new_name='numero',
        ),
        migrations.RemoveField(
            model_name='encaissement',
            name='promotion',
        ),
        migrations.RemoveField(
            model_name='montantcheque',
            name='promotion',
        ),
        migrations.RemoveField(
            model_name='participation',
            name='promotion',
        ),
    ]
