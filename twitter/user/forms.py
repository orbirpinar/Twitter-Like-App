from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from twitterapp.models import Profile

class RegisterForm(UserCreationForm):
	email = forms.EmailField()
	class Meta:
		model = User
		fields = ('username','email','password1','password2')

class UserEditForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username','email','first_name','last_name']

class ProfileEditForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['bio','location','birth_date','image','cover_image']
