from django.urls import path
from . import views

app_name = 'location'

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:traffic_info_id>', views.detail, name='detail'),
    path('search_location', views.search_location),
    path('search_transit_direction', views.search_transit_direction),
    path('db_data', views.db_data, name='db_data'),
    path('db_data/delete_data', views.delete_data),
    path('init_key', views.init_key),
]