from django.urls import path
from . import testViews 
app_name = 'testA'

urlpatterns = [
path('', testViews.index, name='testIndex' ),
path('opt/', testViews.ListPart.as_view(), name = "list_part"),
path('apt<int:pk>', testViews.DetailPart.as_view(), name = 'detail_part'),
]