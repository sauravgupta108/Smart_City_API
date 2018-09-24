from django.urls import path
from . import citySmartViews as views

urlpatterns = [
path('', views.index, name = 'apiHome'),
path('list_of_houses', views.houses_List, name = 'list_of_houses'),
path('list_of_street_lights', views.street_lights_list, name = 'list_of_street_lights'),
path('list_of_dustbins', views.dustbin_list, name = 'list_of_dustbins'),
path('list_of_water_tanks', views.water_tank_list, name = 'list_of_water_tanks'),
path('house/<house_name>', views.House_details.as_view(), name = 'house_detail'),
path('street_light/<light_no>', views.Street_light.as_view(), name = 'house_detail'),
]