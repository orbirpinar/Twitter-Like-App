from django.shortcuts import render,redirect,get_object_or_404
from .forms import RegisterForm,UserEditForm,ProfileEditForm
from django.views import generic
from twitterapp.models import Tweet,Profile
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect


def register(request):
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			return redirect('login')
	else:
		form = RegisterForm()

	return render(request,'user/register.html',{'form':form})
class UserDetailView(generic.ListView):
	model = Tweet
	paginate_by = 10
	context_object_name='user_tweets'
	template_name = 'user/user_detail.html'

	def get_queryset(self):
		user = get_object_or_404(User,username = self.kwargs.get('username'))
		return Tweet.objects.filter(user=user).order_by('-date_created')
	def get_context_data(self,**kwargs):
		context = super(UserDetailView, self).get_context_data(**kwargs)
		user = get_object_or_404(User,username = self.kwargs.get('username'))
		context['profiles']=Profile.objects.filter(user=user)
		context['following'] = Profile.objects.filter(follow=user)
		return context
		
class UserLikesView(generic.ListView):
	model = Tweet
	paginate_by = 10
	context_object_name = "user_likes"
	template_name = 'user/user_likes.html'

	def get_queryset(self):
		user_likes = get_object_or_404(User,username=self.kwargs.get('username'))
		return Tweet.objects.filter(likes=user_likes).order_by('-date_created')
	def get_context_data(self,**kwargs):
		context = super(UserLikesView, self).get_context_data(**kwargs)
		user = get_object_or_404(User,username = self.kwargs.get('username'))
		context['profiles']=Profile.objects.filter(user=user)
		return context

def CreateMessage(request):
	if request.method == "POST":
		form = MessageForm(request.POST)
		if form.is_valid():
			message = form.save(commit=False)
			message.sender = request.user
			message.save()
			return redirect('home')
	else:
		form= MessageForm()
	return render(request,'user/create_message.html',{'form':form})

	
def ProfileEditView(request):
	if request.method == 'POST':
		u_form = UserEditForm(request.POST,instance=request.user)
		p_form = ProfileEditForm(request.POST,request.FILES,instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			return redirect('user-detail',request.user)
	else:
		u_form = UserEditForm(instance=request.user)
		p_form = ProfileEditForm(instance = request.user.profile)
		context = {
		'u_form':u_form,
		'p_form':p_form
		}
		return render(request,'user/profile_edit.html',context)
