# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-10-31 23:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('librarian', '0012_auto_20181030_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='type',
            field=models.CharField(choices=[('A', '教育'), ('B', '计算机'), ('C', '文学'), ('D', '哲学'), ('E', '语言'), ('F', '历史'), ('G', '政治'), ('H', '经济'), ('I', '其他')], max_length=1),
        ),
    ]