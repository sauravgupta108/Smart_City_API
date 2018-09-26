from rest_framework import serializers as SRLZR

from . import models

class Administration_serializer(SRLZR.ModelSerializer):
	class Meta:
		model = models.Administration
		fields = ('username', 'name', 'designation', 'zone_id')