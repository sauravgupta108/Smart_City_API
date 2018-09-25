from django.http import HttpResponse
import copy

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, mixins as MXN
from rest_framework.generics import GenericAPIView as GNVW

from . import models as MDL, Model_Serializers as SRLZR

def index(request):
	return HttpResponse("HEllo....!!!")

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
def houses_List(request):
	list_of_houses = MDL.House.objects.all()
	serialized_list = SRLZR.House_Serializer(list_of_houses, many = True)
	return Response(serialized_list.data)

@api_view()
def zones_List(request):
	list_of_zones = MDL.Zone.objects.all()
	serialized_list = SRLZR.Zone_Serializer(list_of_zones, many = True)
	return Response(serialized_list.data)
	
@api_view()
def street_lights_list(request):
	street_light_list = MDL.Street_light.objects.all()
	serialized_list = SRLZR.Street_light_Serializer(street_light_list, many = True)
	return Response(serialized_list.data)
	
@api_view()
def dustbin_list(request):
	dustbin_list = MDL.Dustbin.objects.all()
	serialized_list = SRLZR.Dustbin_Serializer(dustbin_list, many = True)
	return Response(serialized_list.data)
	
@api_view()
def water_tank_list(request):
	water_tank_list = MDL.Water_tank.objects.all()
	serialized_list = SRLZR.Water_tank_Serializer(water_tank_list, many = True)
	return Response(serialized_list.data)
	
class Street_light(GNVW, MXN.RetrieveModelMixin, MXN.DestroyModelMixin):
	queryset = MDL.Street_light.objects.all()
	lookup_field = 'light_id'
	lookup_url_kwarg = 'light_no'
	
	serializer_class = SRLZR.Street_light_Serializer
	
	def get(self, request, light_no):
		return self.retrieve(request, light_no)
		
	def delete(self, request, light_no):
		return self.destroy(request, light_no)
		
	def patch(self, request, light_no):
		query_set = MDL.Street_light.objects.filter(light_id = light_no)
		
		if query_set.exists() is False:
			return Response({"details":"Invalid light number. Provide correct ID in url"}, status = status.HTTP_400_BAD_REQUEST)
		
		try:
			if request.data['live_status'] not in ["DEAD","SICK","ALIVE"]:
				raise ValueError
			query_set.update(live_status = request.data['live_status'], running_status = request.data['running_status'])
			return self.retrieve(request, light_no)
		except:
			return Response({"live_status":"Valid values are ALIVE, DEAD, SICK","running_status": "valid values are True/1 or False/0" }, status=status.HTTP_400_BAD_REQUEST)
		
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
		return self.retrieve(request, dustbin_id)
		
	def delete(self, request, dustbin_id):
		return self.destroy(request, dustbin_id)
		
	def patch(self, request, dustbin_id):
		query_set = MDL.Dustbin.objects.filter(dustbin_id = dustbin_id)
		
		if query_set.exists() is False:
			return Response({"details":"Invalid Dustbin ID. Provide correct ID in url"}, status = status.HTTP_400_BAD_REQUEST)
		
		try:
			query_set.update(filled_status = request.data['filled_status'])
			return self.retrieve(request, dustbin_id)
		except:
			return Response({"details":"Valid values for filled_stustus: True/1 or False/0"}, status=status.HTTP_400_BAD_REQUEST)
	
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
				return Response({"details":"New Dustbin details added successfully","Dustbin":dustbin_details['dustbin_id']}, \
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
		return self.retrieve(request, water_tank_id)
		
	def delete(self, request, water_tank_id):
		return self.destroy(request, water_tank_id)
		
	def patch(self, request, water_tank_id):
		query_set = MDL.Water_tank.objects.filter(water_tank_id = water_tank_id)
		
		if query_set.exists() is False:
			return Response({"details":"Invalid Water_tank ID. Provide correct ID in url"}, status = status.HTTP_400_BAD_REQUEST)
		
		try:
			if int(request.data['filled_percentage']) > 100:
				raise ValueError
			query_set.update(filled_percentage = request.data['filled_percentage'])
			return self.retrieve(request, water_tank_id)
		except:
			return Response({"filled_percentage":"Integer values between 0-100 are only valid"}, status=status.HTTP_400_BAD_REQUEST)
	
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
				return Response({"details":"New Water Tank details added successfully",'Water_tank':water_tank_details['water_tank_id']}, \
								status = status.HTTP_201_CREATED)
			else:
				raise ValueError
		except (ValueError, KeyError) as error:
			return Response({'street_number':'Positive integers less than 20 are valid',"filled_percentage":"Integer values between 0-100 are only valid"},\
							 status = status.HTTP_400_BAD_REQUEST)
							 
