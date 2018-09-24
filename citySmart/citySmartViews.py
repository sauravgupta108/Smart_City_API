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

@api_view()
def houses_List(request):
	list_of_houses = MDL.House.objects.all()
	serialized_list_of_houses = SRLZR.House_Serializer(list_of_houses, many = True)
	return Response(serialized_list_of_houses.data)

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
	
class House_details(APIView):
	def get_house_details(self, house_name):
		try:
			return MDL.House.objects.get(name = house_name)
		except:
			return None
			
	def get(self, request, house_name, format = None):
		house_detail_obj = self.get_house_details(house_name)
		if house_detail_obj:
			serialized_house_details = SRLZR.House_Serializer(house_detail_obj)
			return Response(serialized_house_details.data)
		else:
			return Response({'status':'404 DoesNotExist'}, status = status.HTTP_404_NOT_FOUND)
			
	def delete(self, request, house_name, format = None):
		house_detail_obj = self.get_house_details(house_name)
		if house_detail_obj:
			house_detail_obj.delete()
			return Response({"message":"Record deleted successfully","House Name": house_name, "Zone" : house_detail_obj.place.zone_id})
		else:
			return Response({'status':'404 DoesNotExist'}, status = status.HTTP_404_NOT_FOUND)
			
	def post(self, request, house_name, format = None):
		house_details = copy.deepcopy(request.data)
		
		try:
			zone = MDL.Zone.objects.get(zone_id = house_details['zone_id'])
		except:
			return Response({"details": "Invalid Zone ID", "status":"400"}, status = status.HTTP_400_BAD_REQUEST)
		
		any_house = MDL.House.objects.filter(place_id = zone.zone_id).order_by('-name')
		new_house_number = None		
		if any_house.exists():
			last_house_number = any_house[0].name
			new_house_number = get_new_number(last_house_number, 4)				
		else:
			zn_part = str(int(zone.zone_id[4:])).zfill(2)
			new_house_number = 'HN'+ zn_part + '0001'
			del(zn_part)
		
		del(house_details['zone_id'])
		house_details['name'] = new_house_number
		house_details['place'] = zone.zone_id
		
		serialized_house_details = SRLZR.House_Serializer(data = house_details)
		if serialized_house_details.is_valid():
			serialized_house_details.save()
			return Response({'status':'201', 'details': "House_details_added_successfully",'house_name':serialized_house_details.data['name']},\
							 status = status.HTTP_201_CREATED)
		else:
			return Response({"details": "Invalid Details", "status":"400"}, status = status.HTTP_400_BAD_REQUEST)

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
		zone = get_zone_and_new_id(light_details['zone_id'])
		
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
		
		serialized_details = SRLZR.Street_light_Serializer(data = light_details)
		if serialized_details.is_valid():
			serialized_details.save()
			return Response({"details":"Light added successfully", "light_ID":light_details['light_id']},\
							status = status.HTTP_201_CREATED)
			
		else:
			return Response({"street_number":"This field is required.","live_status":"Valid values: ALIVE, DEAD, SICK"},\
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
	
