from . import admin_views as VW
from django.urls import path

urlpatterns = [
path('', VW.test, name = 'test'),
path('authenticate', VW.Authentication.as_view(), name = 'authenticate'),
]

