from django.urls import path
from . import citySmartViews as views, zhp_views as zhp

urlpatterns = [
path('', views.index, name = 'apiHome'),
path('zones', views.zones_List, name = 'zones'),
path('houses', views.houses_List, name = 'houses'),
path('street_lights', views.street_lights_list, name = 'street_lights'),
path('dustbins', views.dustbin_list, name = 'dustbins'),
path('water_tanks', views.water_tank_list, name = 'water_tanks'),
path('house/<house_number>', zhp.House.as_view(), name = 'house_detail'),
path('street_light/<light_no>', views.Street_light.as_view(), name = 'house_detail'),
path('dustbin/<dustbin_id>', views.Dustbin.as_view(), name = 'house_detail'),
path('water_tank/<water_tank_id>', views.Water_tank.as_view(), name = 'house_detail'),
]