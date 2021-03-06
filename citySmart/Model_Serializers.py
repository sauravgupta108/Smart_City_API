from rest_framework import serializers as SRLZR
from . import models

class Person_Serializer(SRLZR.ModelSerializer):
	class Meta:
		model = models.Person
		fields = ('name', 'profession', 'house')
		
class House_Serializer(SRLZR.ModelSerializer):
	class Meta:
		model = models.House
		fields = ('house_id','spoc', 'no_of_vehicles', 'street_number', 'place')
		
class Zone_Serializer(SRLZR.ModelSerializer):
	class Meta:
		model = models.Zone
		fields = ('zone_id','name', 'person_incharge')
		
class Street_light_Serializer(SRLZR.ModelSerializer):
	class Meta:
		model = models.Street_light
		fields = ('light_id', 'street_number', 'health', 'running_status', 'zone')
		
class Dustbin_Serializer(SRLZR.ModelSerializer):
	class Meta:
		model = models.Dustbin
		fields = ('dustbin_id', 'street_number','filled_status', 'zone')
		
class Water_tank_Serializer(SRLZR.ModelSerializer):
	class Meta:
		model = models.Water_tank
		fields = ('water_tank_id', 'street_number', 'filled_percentage', 'zone')