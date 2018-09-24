from django.db import models

# Create your models here.
class testapi(models.Model):
	id = models.AutoField(primary_key = True)
	date_of_birth = models.DateField(auto_now=False, blank = True)
	name = models.CharField(max_length = 20)