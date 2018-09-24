from . import testModels
from rest_framework import serializers

class SrlzdTestapi(serializers.ModelSerializer):
	class Meta:
		model = testModels.testapi
		fields = ('id','date_of_birth', 'name')
		
	def validity(self):
		if int(self.initial_data['date_of_birth'].split('-')[0]) <= 1999:
			return True
		return False;