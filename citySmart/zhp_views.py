import copy

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, mixins as MXN
from rest_framework.generics import GenericAPIView as GNVW

from . import models as MDL, Model_Serializers as SRLZR
from api_security.security import Token_handler as tkn

class Zone(GNVW, MXN.RetrieveModelMixin, MXN.DestroyModelMixin):
	queryset = MDL.Zone.objects.all()
	lookup_field = 'zone_id'
	lookup_url_kwarg = 'zone_id'
	
	serializer_class = SRLZR.Zone_Serializer
	
	def get(self, request, zone_id):
		tkn().update_token_history(request.query_params['client_id'], "GET", 'Zone : ' + zone_id)
		return self.retrieve(request, zone_id)
			
	def delete(self, request, zone_id):
		tkn().update_token_history(request.query_params['client_id'], "DELETE", 'Zone : ' + zone_id)
		return self.destroy(request, zone_id)
			
	def put(self, request, zone_id, format = None):
		try:
			zone = MDL.Zone.objects.get(zone_id = zone_id)
		except:
			return Response({"detail":"Invalid Zone_id"}, status = status.HTTP_400_BAD_REQUEST)

		try:
			name = request.data["incharge"]
			if not is_valid_name(name):
				raise ValueError("Invalid Name")

			zone.person_incharge = name
			zone.save()
			tkn().update_token_history(request.query_params['client_id'], "UPDATE", 'Zone : ' + zone_id)
			return self.retrieve(request, zone_id)
		except ValueError:
			return Response({"detail" : "Invalid Name."}, status = status.HTTP_400_BAD_REQUEST)
		except KeyError:
			return Response({"detail" : "Incharge name is None."}, status = status.HTTP_400_BAD_REQUEST)

def is_valid_name(name = "123"):
	parts = name.split(" ")
	for part in parts:
		if not part.isalpha():
			return False
	return True

class House(GNVW, MXN.RetrieveModelMixin, MXN.DestroyModelMixin):
	queryset = MDL.House.objects.all()
	lookup_field = 'house_id'
	lookup_url_kwarg = 'house_number'
	
	serializer_class = SRLZR.House_Serializer
	
	def get(self, request, house_number):
		tkn().update_token_history(request.query_params['client_id'], "GET", 'House : ' + house_number)
		return self.retrieve(request, house_number)
			
	def delete(self, request, house_number):
		tkn().update_token_history(request.query_params['client_id'], "DELETE", 'House : ' + house_number)
		return self.destroy(request, house_number)
			
	def post(self, request, house_name, format = None):
		pass

class Person:
	pass