# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from ..registry import registry


FILTER_CHOICES = registry.get_filter_choices()


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TextFilter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort', models.SmallIntegerField(verbose_name='Sort')),
                ('name', models.CharField(max_length=50, verbose_name='Select Filter', choices=FILTER_CHOICES)),
            ],
        ),
        migrations.CreateModel(
            name='TextFormat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('slug', models.SlugField(unique=True, verbose_name='Machine Name')),
            ],
        ),
        migrations.AddField(
            model_name='textfilter',
            name='format',
            field=models.ForeignKey(related_name='filters', to='django_textformat.TextFormat'),
        ),
    ]
