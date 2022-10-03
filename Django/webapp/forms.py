from django.forms import ModelForm
from django import forms
from django.conf import settings
from .models import signup
# from passlib.hash import pbkdf2_sha256


class SignupForm(forms.ModelForm):
	Password = forms.CharField(widget = forms.PasswordInput)
	# enc_password = pbkdf2_sha256.encrypt(Password,rounds=12000,salt_size=32)
	ConfirmPassword = forms.CharField(widget = forms.PasswordInput)
	# enc_confirmpassword = pbkdf2_sha256.encrypt(ConfirmPassword,rounds=12000,salt_size=32)
	class Meta:
		model = signup
		fields = ['FirstName', 'LastName', 'Email', 'UserName', 'PhoneNumber', 'Password', 'ConfirmPassword']
		# fields = ['FirstName', 'LastName', 'Email', 'UserName', 'PhoneNumber', 'Password', 'ConfirmPassword','ConfirmationCode']
		labels = {'FirstName':'First Name', 'LastName':'Last Name', 'Email':'Email', 'UserName':'User Name', 'PhoneNumber':'Phone Number', 'Password': 'Password', 'ConfirmPassword':'ConfirmPassword'}


