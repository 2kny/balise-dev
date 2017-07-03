# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-02 09:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('compta', '0007_auto_20170625_1504'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eleve',
            name='promotion',
        ),
        migrations.RemoveField(
            model_name='eleve',
            name='user',
        ),
        migrations.AlterField(
            model_name='binet',
            name='current_president',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='current_president', to='accounts.Eleve', verbose_name='Président'),
        ),
        migrations.AlterField(
            model_name='binet',
            name='current_promotion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Promotion', verbose_name='Promo'),
        ),
        migrations.AlterField(
            model_name='binet',
            name='current_tresorier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='current_tresorier', to='accounts.Eleve', verbose_name='Trésorier'),
        ),
        migrations.AlterField(
            model_name='lignecompta',
            name='auteur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Eleve', verbose_name='Par'),
        ),
        migrations.AlterField(
            model_name='mandat',
            name='president',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='president', to='accounts.Eleve'),
        ),
        migrations.AlterField(
            model_name='mandat',
            name='tresorier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tresorier', to='accounts.Eleve'),
        ),
        migrations.DeleteModel(
            name='Eleve',
        ),
        migrations.DeleteModel(
            name='Promotion',
        ),
    ]
