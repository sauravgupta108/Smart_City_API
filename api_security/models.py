from django.db import models
from citySmart.models import Zone

# Create your models here.
class Administration(models.Model):
	position = (('Secretary','Secretary'),('ZoneHead', 'ZoneHead'))
	username = models.CharField(max_length = 10, primary_key = True)
	password = models.CharField(max_length = 40)
	name = models.CharField(max_length = 30)
	designation = models.CharField(max_length = 12, choices = position)
	secret_key = models.CharField(max_length = 16, unique = True)
	zone = models.ForeignKey(Zone, on_delete = models.CASCADE)
	
class Token(models.Model):
	user = models.OneToOneField(Administration, on_delete = models.CASCADE)
	key = models.CharField(max_length = 10, unique = True)
	value = models.CharField(max_length = 50, unique = True)
	
class Token_usage_history(models.Model):
	user = models.ForeignKey(Administration, on_delete = models.CASCADE)
	operation = models.CharField(max_length = 8)
	summary = models.CharField(max_length = 30)
	date = models.DateTimeField(auto_now = True)