from django.http import HttpResponse
from django.core.exceptions import ValidationError
import copy, base64
from . import models_helper as mh

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, mixins as MXN
from rest_framework.generics import GenericAPIView as GNVW

from . import models as MDL, Model_Serializers as SRLZR
from api_security.security import Token_handler as tkn

def index(request):
	return HttpResponse("Hello....!!!")

def get_new_number(str_number, padding): #HN010002, 4 
	num_part = int(str_number[len(str_number)-padding:])+1
	str_part = str_number[:len(str_number)-padding]
	return str_part + str(num_part).zfill(padding)
	
def get_zone(zone_id):
	query_set = MDL.Zone.objects.filter(zone_id = zone_id)
	if query_set.exists():
		return query_set[0]
	else:
		return None

@api_view()
def houses_list(request):
	list_of_houses = MDL.House.objects.all()
	serialized_list = SRLZR.House_Serializer(list_of_houses, many = True)
	return Response(serialized_list.data)

@api_view()
def zones_list(request):
	list_of_zones = MDL.Zone.objects.all()
	serialized_list = SRLZR.Zone_Serializer(list_of_zones, many = True)
	return Response(serialized_list.data)
	
@api_view()
def street_lights_list(request):	
	street_light_list = MDL.Street_light.objects.all()
	
	# Filters
	try:
		if "sn" in request.query_params:		
			street_light_list = street_light_list.filter(street_number = int(request.query_params["sn"]))		
	
		if "hlth" in request.query_params:
			street_light_list = street_light_list.filter(health = int(request.query_params["hlth"]))

		if "rs" in request.query_params:
			street_light_list = street_light_list.filter(running_status = request.query_params["rs"])

		if "zn" in request.query_params:
			street_light_list = street_light_list.filter(zone = request.query_params["zn"])

		if street_light_list.count() == 0:
			raise TypeError
	except:
		return Response([])

	serialized_list = SRLZR.Street_light_Serializer(street_light_list, many = True)
	return Response(serialized_list.data)
	
@api_view()
def dustbin_list(request):
	dustbin_list = MDL.Dustbin.objects.all()

	# Filters
	if "sn" in request.query_params:
		try:
			dustbin_list = dustbin_list.filter(street_number = int(request.query_params["sn"]))
		except ValueError:
			return Response([])
	
	if "fs" in request.query_params:
		try:
			dustbin_list = dustbin_list.filter(filled_status = request.query_params["fs"])
		except:
			return Response([])

	if "zn" in request.query_params:
		dustbin_list = dustbin_list.filter(zone = request.query_params["zn"])

	serialized_list = SRLZR.Dustbin_Serializer(dustbin_list, many = True)
	return Response(serialized_list.data)
	
@api_view()
def water_tank_list(request):
	water_tank_list = MDL.Water_tank.objects.all()

	# Filters
	if "sn" in request.query_params:
		try:
			water_tank_list = water_tank_list.filter(street_number = int(request.query_params["sn"]))
		except ValueError:
			return Response([])
	
	if "fp" in request.query_params:
		try:
			water_tank_list = water_tank_list.filter(filled_percentage = int(request.query_params["fp"]))
		except ValueError:
			return Response([])
	if "fp_gt" in request.query_params:
		try:
			water_tank_list = water_tank_list.filter(filled_percentage__gte = int(request.query_params["fp"]))
		except ValueError:
			return Response([])

	if "fp_lt" in request.query_params:
		try:
			water_tank_list = water_tank_list.filter(filled_percentage__lte = int(request.query_params["fp"]))
		except ValueError:
			return Response([])

	if "zn" in request.query_params:
		water_tank_list = water_tank_list.filter(zone = request.query_params["zn"])

	serialized_list = SRLZR.Water_tank_Serializer(water_tank_list, many = True)
	return Response(serialized_list.data)
	
class Street_light(GNVW, MXN.RetrieveModelMixin, MXN.DestroyModelMixin):
	queryset = MDL.Street_light.objects.all()
	lookup_field = 'light_id'
	lookup_url_kwarg = 'light_no'
	
	serializer_class = SRLZR.Street_light_Serializer
	
	def get(self, request, light_no):
		tkn().update_token_history(request.query_params['client_id'], 'GET', 'light : ' + light_no)
		return self.retrieve(request, light_no)

	def delete(self, request, light_no):
		tkn().update_token_history(request.query_params['client_id'], "DELETE", 'light : ' + light_no)
		return self.destroy(request, light_no)
		
	def patch(self, request, light_no):		
		try:
			light = MDL.Street_light.objects.get(light_id = light_no)
		except:
			return Response({"detail":"Invalid Street_light ID."}, status = status.HTTP_400_BAD_REQUEST)
		
		try:
			health_status = int(request.data['health'])
			if health_status not in [mh.LIGHT_ALIVE, mh.LIGHT_SICK, mh.LIGHT_DEAD]:
				raise ValueError
			
			light.health = health_status
			light.running_status = request.data['running_status']
			
			if health_status == mh.LIGHT_DEAD:
				light.running_status = False
			
			light.save()
			tkn().update_token_history(request.query_params['client_id'], 'UPDATE', 'light : ' + light_no)
			return self.retrieve(request, light_no)
		except KeyError:
			return Response({"detail" : "Health and running_status can't be None."}, status=status.HTTP_400_BAD_REQUEST)
		except ValueError:
			return Response({"detail" : "Invalid Health status"}, status=status.HTTP_400_BAD_REQUEST)
		except ValidationError:
			return Response({"detail" : "running_status - valid values are True/1 or False/0"}, status=status.HTTP_400_BAD_REQUEST)

	def post(self, request, light_no):
		light_details = copy.deepcopy(request.data)
		zone = get_zone(light_details['zone_id'])
		
		if zone is None:
			return Response({"details":"Invalid zone id"}, status = status.HTTP_400_BAD_REQUEST)
		
		any_light = MDL.Street_light.objects.all().order_by("-light_id")
		if any_light.exists():
			last_light_number = any_light[0].light_id
			new_light_number = get_new_number(last_light_number, 3)				
		else:
			new_light_number = 'SL001'			
		
		del(light_details['zone_id'])
		light_details['light_id'] = new_light_number
		light_details['zone'] = zone.zone_id
		
		try:
			if int(light_details['street_number']) > 20 or int(light_details['street_number']) == 0:   #Hard codded value
				raise ValueError
		
			serialized_details = SRLZR.Street_light_Serializer(data = light_details)
			if serialized_details.is_valid():
				serialized_details.save()
				tkn().update_token_history(request.query_params['client_id'], 'ADD', 'light : ' + new_light_number)
				return Response({"details":"Light added successfully", "light_ID":light_details['light_id']},\
								status = status.HTTP_201_CREATED)
				
			else:
				raise ValueError
		except ValueError:
			return Response({"street_number":"Positive integers less than 20 are valid.","live_status":"Valid values: ALIVE, DEAD, SICK"},\
							status = status.HTTP_400_BAD_REQUEST)
	
class Dustbin(GNVW, MXN.RetrieveModelMixin, MXN.DestroyModelMixin):
	queryset = MDL.Dustbin.objects.all()
	lookup_field = 'dustbin_id'
	lookup_url_kwarg = 'dustbin_id'
	
	serializer_class = SRLZR.Dustbin_Serializer
	
	def get(self, request, dustbin_id):
		tkn().update_token_history(request.query_params['client_id'], "GET", 'Dustbin : ' + dustbin_id)
		return self.retrieve(request, dustbin_id)
		
	def delete(self, request, dustbin_id):
		tkn().update_token_history(request.query_params['client_id'], "DELETE", 'Dustbin : ' + dustbin_id)
		return self.destroy(request, dustbin_id)
		
	def patch(self, request, dustbin_id):
		try:
			dustbin = MDL.Dustbin.objects.get(dustbin_id = dustbin_id)
		except:
			return Response({"detail":"Invalid Dustbin ID."}, status = status.HTTP_400_BAD_REQUEST)
		
		try:
			dustbin.filled_status = request.data['filled_status']
			dustbin.save()
			tkn().update_token_history(request.query_params['client_id'], "UPDATE", 'Dustbin : ' + dustbin_id)
			return self.retrieve(request, dustbin_id)
		except KeyError:
			return Response({"detail" : "filled_status is None."}, status = status.HTTP_400_BAD_REQUEST)
		except ValidationError:
			return Response({"detail":"Valid values for filled_status (True/1 or False/0)"}, status=status.HTTP_400_BAD_REQUEST)					
	
	def post(self, request, dustbin_id):
		dustbin_details = copy.deepcopy(request.data)
		zone = get_zone(dustbin_details['zone_id'])
		if zone is None:
			return Response({'details':"Invalid zone_id"}, status = status.HTTP_400_BAD_REQUEST)
		
		any_dustbin = MDL.Dustbin.objects.all().order_by("-dustbin_id")
		if any_dustbin.exists():
			new_dustbin = get_new_number(any_dustbin[0].dustbin_id, 7)
		else:
			new_dustbin = 'dbn0000001'
		
		dustbin_details['dustbin_id'] = new_dustbin
		dustbin_details['zone'] = zone.zone_id
		del(dustbin_details['zone_id'])
		
		try:
			if int(dustbin_details['street_number']) > 20 or int(dustbin_details['street_number']) == 0:   #Hard codded value
				raise ValueError
			
			serialized_details = self.serializer_class(data = dustbin_details)
			if serialized_details.is_valid():
				serialized_details.save()
				tkn().update_token_history(request.query_params['client_id'], "ADD", 'Dustbin : ' + new_dustbin)
				return Response({"detail":"New Dustbin details added successfully","Dustbin":dustbin_details['dustbin_id']}, \
								status = status.HTTP_201_CREATED)
			else:
				raise ValueError
		except (ValueError, KeyError) as error:
			return Response({'street_number':'Positive integers less than 20 are valid','filled_status':'True/1 or False/0 are valid'},\
							status = status.HTTP_400_BAD_REQUEST)
	
class Water_tank(GNVW, MXN.RetrieveModelMixin, MXN.DestroyModelMixin):
	queryset = MDL.Water_tank.objects.all()
	lookup_field = 'water_tank_id'
	lookup_url_kwarg = 'water_tank_id'
	
	serializer_class = SRLZR.Water_tank_Serializer
	
	def get(self, request, water_tank_id):
		tkn().update_token_history(request.query_params['client_id'], "GET", 'Water_tank : ' + water_tank_id)
		return self.retrieve(request, water_tank_id)
		
	def delete(self, request, water_tank_id):
		tkn().update_token_history(request.query_params['client_id'], "DELETE", 'Water_tank : ' + water_tank_id)
		return self.destroy(request, water_tank_id)
		
	def patch(self, request, water_tank_id):
		try:
			tank = MDL.Water_tank.objects.get(water_tank_id = water_tank_id)
		except:
			return Response({"detail":"Invalid Water_tank ID."}, status = status.HTTP_400_BAD_REQUEST)
		
		try:
			if int(request.data['filled_percentage']) > 100:
				raise ValueError
			tank.filled_percentage = request.data['filled_percentage']
			tank.save()
			tkn().update_token_history(request.query_params['client_id'], "UPDATE", 'Water_tank : ' + water_tank_id)
			return self.retrieve(request, water_tank_id)
		except KeyError:
			return Response({"detail" : "filled_percentage is None."}, status = status.HTTP_400_BAD_REQUEST)
		except ValueError:
			return Response({"filled_percentage":"Only integer values between 0-100 are valid"}, status=status.HTTP_400_BAD_REQUEST)
	
	def post(self, request, water_tank_id):
		water_tank_details = copy.deepcopy(request.data)
		
		zone = get_zone(water_tank_details['zone_id'])
		if zone is None:
			return Response({'details':"Invalid zone_id"}, status = status.HTTP_400_BAD_REQUEST)
		
		any_water_tank = MDL.Water_tank.objects.all().order_by("-water_tank_id")
		if any_water_tank.exists():
			new_water_tank = get_new_number(any_water_tank[0].water_tank_id, 6)
		else:
			new_water_tank = 'tank000001'
		
		water_tank_details['water_tank_id'] = new_water_tank
		water_tank_details['zone'] = zone.zone_id
		del(water_tank_details['zone_id'])
		
		try:
			if int(water_tank_details['street_number']) > 20 or int(water_tank_details['street_number']) == 0:   #Hard codded value
				raise ValueError
			if int(water_tank_details['filled_percentage']) > 100:
				raise ValueError
			
			serialized_details = self.serializer_class(data = water_tank_details)
			if serialized_details.is_valid():
				serialized_details.save()
				tkn().update_token_history(request.query_params['client_id'], "ADD", 'Water_tank : ' + new_water_tank)
				return Response({"detail":"New Water Tank details added successfully",'Water_tank':water_tank_details['water_tank_id']}, \
								status = status.HTTP_201_CREATED)
			else:
				raise ValueError
		except (ValueError, KeyError) as error:
			return Response({'street_number':'Positive integers less than 20 are valid',"filled_percentage":"Integer values between 0-100 are only valid"},\
							 status = status.HTTP_400_BAD_REQUEST)
	
