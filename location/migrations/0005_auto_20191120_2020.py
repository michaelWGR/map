# Generated by Django 2.2.7 on 2019-11-20 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0004_auto_20191109_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keymsg',
            name='created_time',
            field=models.DateTimeField(default='2019-11-20 20:20:29', verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='keymsg',
            name='is_deleted',
            field=models.IntegerField(default=0, verbose_name='是否已删除，0：未删除，1：已删除'),
        ),
        migrations.AlterField(
            model_name='keymsg',
            name='modified_time',
            field=models.DateTimeField(default='2019-11-20 20:20:29', verbose_name='修改时间'),
        ),
        migrations.AlterField(
            model_name='keymsg',
            name='type',
            field=models.IntegerField(default=0, verbose_name='key的类型，0：高德地图'),
        ),
    ]
