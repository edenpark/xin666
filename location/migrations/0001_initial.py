# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-01 22:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import location.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('weibousers', '0003_auto_20170131_1936'),
        ('categories', '0003_auto_20170301_2215'),
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=120)),
                ('poiid', models.CharField(db_index=True, max_length=120)),
                ('province', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('city', models.PositiveSmallIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weibo_id', models.BigIntegerField(blank=True, null=True, unique=True)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('text', models.TextField(blank=True, null=True)),
                ('weibo_img', models.URLField(blank=True, max_length=150, null=True)),
                ('weibo_thumb_img', models.URLField(blank=True, max_length=150, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=location.models.image_path)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='categories.Category')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.Place')),
                ('second_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='second_category_post', to='categories.Category', verbose_name=b'2nd category')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='SubPlace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=120)),
                ('poiid', models.CharField(db_index=True, max_length=120)),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.Place')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='sub_place',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='location.SubPlace'),
        ),
        migrations.AddField(
            model_name='post',
            name='third_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='third_category_post', to='categories.Category', verbose_name=b'3rd category'),
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weibousers.WeiboUser'),
        ),
    ]
