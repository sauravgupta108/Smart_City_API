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
	
	def get(self, request, house_name):
		return self.retrieve(request, house_name)
			
	def delete(self, request, house_name):
		return self.destroy(request, house_name)
			
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