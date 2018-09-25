import copy

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, mixins as MXN
from rest_framework.generics import GenericAPIView as GNVW

from . import models as MDL, Model_Serializers as SRLZR

class Zone(GNVW, MXN.RetrieveModelMixin, MXN.DestroyModelMixin):
	queryset = MDL.Zone.objects.all()
	lookup_field = 'zone_id'
	lookup_url_kwarg = 'zone_id'
	
	serializer_class = SRLZR.Zone_Serializer
	
	def get(self, request, zone_id):
		return self.retrieve(request, zone_id)
			
	def delete(self, request, zone_id):
		return self.destroy(request, zone_id)
			
	def post(self, request, zone_id, format = None):
		pass

class House(GNVW, MXN.RetrieveModelMixin, MXN.DestroyModelMixin):
	queryset = MDL.House.objects.all()
	lookup_field = 'house_id'
	lookup_url_kwarg = 'house_number'
	
	serializer_class = SRLZR.House_Serializer
	
	def get(self, request, house_number):
		return self.retrieve(request, house_number)
			
	def delete(self, request, house_number):
		return self.destroy(request, house_number)
			
	def post(self, request, house_name, format = None):
		pass