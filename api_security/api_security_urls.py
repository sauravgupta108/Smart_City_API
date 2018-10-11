from . import admin_views as VW
from django.urls import path

urlpatterns = [
path('authenticate', VW.Authentication.as_view(), name = 'authenticate'),
]

#path('', VW.test, name = 'test'),