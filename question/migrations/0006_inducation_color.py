# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-02-26 02:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0005_inducation_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='inducation',
            name='color',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='类型颜色'),
        ),
    ]
