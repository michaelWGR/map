from django.urls import path
from . import views

app_name = 'location'

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:traffic_info_id>', views.detail, name='detail'),
    path('search_location', views.search_location),
    path('search_transit_direction', views.search_transit_direction),
    path('transit', views.transit_direction, name='transit'),
]