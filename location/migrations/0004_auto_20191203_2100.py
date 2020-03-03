# Generated by Django 2.2.7 on 2019-12-03 13:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0003_auto_20191203_2057'),
    ]

    operations = [
        migrations.AddField(
            model_name='transit_detail',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 3, 13, 0, 44, 994332, tzinfo=utc), verbose_name='创建时间'),
        ),
        migrations.AddField(
            model_name='transit_detail',
            name='modified_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 3, 13, 0, 44, 994332, tzinfo=utc), verbose_name='修改时间'),
        ),
        migrations.AlterField(
            model_name='circle',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 3, 13, 0, 44, 993332, tzinfo=utc), verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='circle',
            name='modified_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 3, 13, 0, 44, 992332, tzinfo=utc), verbose_name='修改时间'),
        ),
        migrations.AlterField(
            model_name='keymsg',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 3, 13, 0, 44, 992332, tzinfo=utc), verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='keymsg',
            name='modified_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 3, 13, 0, 44, 992332, tzinfo=utc), verbose_name='修改时间'),
        ),
        migrations.AlterField(
            model_name='traffic_info',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 3, 13, 0, 44, 993332, tzinfo=utc), verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='traffic_info',
            name='modified_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 3, 13, 0, 44, 993332, tzinfo=utc), verbose_name='修改时间'),
        ),
    ]