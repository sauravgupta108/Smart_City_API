import copy

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, mixins as MXN
from rest_framework.generics import GenericAPIView as GNVW

from . import models as MDL, Model_Serializers as SRLZR

class House(GNVW, MXN.RetrieveModelMixin, MXN.DestroyModelMixin):
	queryset = MDL.House.objects.all()
	lookup_field = 'name'
	lookup_url_kwarg = 'house_name'
	
	serializer_class = SRLZR.House_Serializer
	
	def get(self, request, house_number):
		return self.retrieve(request, house_number)
			
	def delete(self, request, house_number):
		return self.destroy(request, house_number)
			
	def post(self, request, house_name, format = None):
		pass