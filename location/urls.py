from django.urls import path
from . import views

app_name = 'location'

urlpatterns = [
    path('', views.index, name='index'),
    path('locate', views.locate, name='locate'),
    path('transit', views.transit_direction, name='transit'),
    path('detail/(<int:traffic_info_id>)', views.detail, name='detail'),
]