from django import forms
from .models import Tweet,Reply

class TweetForm(forms.ModelForm):
	content = forms.CharField(widget=forms.Textarea(attrs={'class':'content-input',
		'placeholder':"What's Happening?",}),label="")
	
	class Meta:
		model = Tweet
		fields = ['content','image']
		

class ReplyForm(forms.ModelForm):
	content = forms.CharField(widget=forms.Textarea(attrs={'class':'content-input',
		'placeholder':"Tweet your reply",}),label="")
	
	class Meta:
		model = Reply	
		fields = ['content']

        
