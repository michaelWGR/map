from django.db import models
import time

# Create your models here.

class Keymsg(models.Model):
    key = models.CharField(max_length=100, verbose_name='api的请求key')
    type = models.IntegerField(default=0, verbose_name='key的类型，0：高德地图')
    is_deleted = models.IntegerField(default=0, verbose_name='是否已删除，0：未删除，1：已删除')
    modified_time = models.DateTimeField(default=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), verbose_name='修改时间')
    created_time = models.DateTimeField(default=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), verbose_name='创建时间')

    def __str__(self):
        return self.key