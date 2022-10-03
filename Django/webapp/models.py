from django.db import models
from django.conf import settings



class signup(models.Model):
	FirstName = models.CharField(max_length = 20)
	LastName = models.CharField(max_length = 20)
	Email = models.EmailField(max_length = 35,unique = True)
	UserName = models.CharField(max_length = 20,unique = True)
	PhoneNumber = models.CharField(max_length = 20)
	Password = models.CharField(max_length = 256)
	ConfirmPassword = models.CharField(max_length = 256)
	ConfirmationCode = models.CharField(max_length = 10,default = "89965")

class Profile(models.Model):
	FirstName = models.CharField(max_length = 20)
	LastName = models.CharField(max_length = 20)
	Email = models.EmailField(max_length = 35,unique = True)
	UserName = models.CharField(max_length = 20,unique = True)
	PhoneNumber = models.CharField(max_length = 20)
	
	
	

