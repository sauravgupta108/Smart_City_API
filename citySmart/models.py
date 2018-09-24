from django.db import models

class Person(models.Model):
	aadhar_number = models.DecimalField(max_digits=12, decimal_places = 0, primary_key = True)
	name = models.CharField(max_length=30)
	date_of_birth = models.DateField(auto_now=False)
	profession = models.CharField(max_length=20, blank = True)
	email = models.EmailField(max_length = 50, blank = True)
	mobile_number = models.DecimalField(max_digits=10, decimal_places=0, blank = True)
	residence = models.ForeignKey('House', on_delete = models.CASCADE)
	
	
class House(models.Model):
	name = models.CharField(max_length=10, primary_key=True)
	no_of_residents = models.PositiveSmallIntegerField()
	no_of_vehicles = models.PositiveSmallIntegerField()
	street_number = models.PositiveSmallIntegerField()
	place = models.ForeignKey('Zone', on_delete = models.CASCADE)
	
class Zone(models.Model):
	zone_id = models.CharField(max_length = 10, primary_key = True)
	name = models.CharField(max_length=20)
	person_incharge = models.CharField(max_length = 30)
	
	def __str__(self):
		return str({'id':self.zone_id, 'name':self.name, 'incharge':self.person_incharge})
	
class Street_light(models.Model):
	LIVE_CHOICES = (('ALIVE','alive'),('SICK', 'sick'),('DEAD','dead'))
	light_id = models.CharField(max_length=5, primary_key=True)
	street_number = models.PositiveSmallIntegerField()
	live_status = models.CharField(max_length=5, choices=LIVE_CHOICES, default='DEAD')
	running_status = models.BooleanField(default=False)
	zone = models.ForeignKey('Zone', on_delete=models.CASCADE)
	
class Dustbin(models.Model):
	dustbin_id = models.CharField(max_length=10, primary_key=True)
	street_number = models.PositiveSmallIntegerField()
	filled_status = models.BooleanField(default=False)
	zone = models.ForeignKey('Zone', on_delete=models.CASCADE)
	
class Water_tank(models.Model):
	water_tank_id = models.CharField(max_length=10, primary_key=True)
	street_number = models.PositiveSmallIntegerField()
	filled_percentage = models.PositiveSmallIntegerField()
	zone = models.ForeignKey('Zone', on_delete=models.CASCADE)
	
	
	
	
