from django.db import models
import time

class Keymsg(models.Model):
    key = models.CharField(max_length=100, verbose_name='api的请求key')
    type = models.IntegerField(default=0, verbose_name='key的类型，0：高德地图')
    is_deleted = models.IntegerField(default=0, verbose_name='是否已删除，0：未删除，1：已删除')
    modified_time = models.DateTimeField(default=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                         verbose_name='修改时间')
    created_time = models.DateTimeField(default=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                        verbose_name='创建时间')

    def __str__(self):
        return self.key

class Circle(models.Model):
    center_location = models.CharField(max_length=50, verbose_name='圆心的经纬度')
    radius = models.IntegerField(verbose_name='圆的半径')
    modified_time = models.DateTimeField(default=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                         verbose_name='修改时间')
    created_time = models.DateTimeField(default=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                        verbose_name='创建时间')

    def __str__(self):
        return self.id

class Traffic_info(models.Model):
    name = models.CharField(max_length=50, verbose_name='交通名称')
    location = models.CharField(max_length=50, verbose_name='交通经纬度')
    circle = models.ForeignKey(Circle, on_delete=models.CASCADE)
    modified_time = models.DateTimeField(default=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                         verbose_name='修改时间')
    created_time = models.DateTimeField(default=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                        verbose_name='创建时间')

    def __str__(self):
        return self.name

class Transit_detail(models.Model):
    traffic_info = models.ForeignKey(Traffic_info, on_delete=models.CASCADE)
    circle = models.ForeignKey(Circle, on_delete=models.CASCADE, default=None)
    total_per_cost = models.FloatField(max_length=10, verbose_name='总平均费用（元）')
    total_per_duration = models.FloatField(max_length=10, verbose_name='总平均时间（秒）')
    total_per_walking_distance = models.FloatField(max_length=10, verbose_name='总平均步行路程（米）')
    total_per_distance =models.FloatField(max_length=10, verbose_name='总平均距离（米）')
    detail = models.TextField(verbose_name='路程详细信息')
    around_market = models.TextField(verbose_name='周边超市')
    around_housing = models.TextField(verbose_name='周边公寓')

    def __str__(self):
        return self.id