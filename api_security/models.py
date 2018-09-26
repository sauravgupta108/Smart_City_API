from django.db import models
from citySmart.models import Zone

# Create your models here.
class Administration(models.Model):
	position = (('Secretary','Secretary'),('ZoneHead', 'ZoneHead'))
	username = models.CharField(max_length = 10, primary_key = True)
	password = models.CharField(max_length = 40)
	name = models.CharField(max_length = 30)
	designation = models.CharField(max_length = 12, choices = position)
	zone = models.ForeignKey(Zone, on_delete = models.CASCADE)