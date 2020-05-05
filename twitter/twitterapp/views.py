from itertools import chain
from django.shortcuts import render, redirect,get_object_or_404
from .models import Tweet,Reply,Profile,RetweetModel,Post
from .forms import TweetForm,ReplyForm
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.http import HttpResponseRedirect,JsonResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic.edit import FormMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.views import View
from django.forms.models import model_to_dict
from django.core import serializers

def landing(request):
	if request.user.is_authenticated:
		return redirect('home')
	return render(request,'twitterapp/landing.html')
	


@login_required
def home(request):
	following = Profile.objects.filter(follow=request.user)
	posts = Post.objects.select_related('tweet','retweetmodel').all().order_by('-date_created')

	page = request.GET.get('page',1)
	paginator = Paginator(posts,10)
	try:
		tweet = paginator.page(page)
	except PageNotAnInteger:
		tweet = paginator.page(1)
	except EmptyPage:
		tweet = paginator.page(paginator.num_pages)

	if request.method == "POST":
		form = TweetForm(request.POST,request.FILES)
		if form.is_valid():
			create_tweet = form.save(commit=False)
			create_tweet.user = request.user
			create_tweet.save()
			return redirect('home')
	else:	
		form = TweetForm()
	
	return render(request,'twitterapp/home.html',{'posts':posts,'form':form,'following':following})


def like_tweet(request):
	tweet_id = request.GET.get('id')
	action = request.GET.get('action')	
	tweet = get_object_or_404(Tweet,id=tweet_id)
	is_liked= False
	if request.user in tweet.likes.all():
		
		tweet.likes.remove(request.user)
		is_liked = False
	else:
		tweet.likes.add(request.user)
		is_liked=True

	#send to previous page
	return JsonResponse({'is_liked':is_liked})

def retweet(request):
	tweet = get_object_or_404(Tweet,id=request.POST.get('id'))
	#if user already retweet the tweet, this will remove the Retweet from 
	

	is_retweet = False
	if RetweetModel.objects.filter(user=request.user,retweet=tweet).exists():
		RetweetModel.objects.filter(user=request.user,retweet=tweet).delete()
		is_retweet = False
		return JsonResponse({"is_retweet":is_retweet})
	else:
		if request.method=="POST":
			new_retweet = RetweetModel(user=request.user,retweet=tweet)
			new_retweet.save()
			is_retweet = True
			return JsonResponse({
		"is_retweet":is_retweet,
		"new_retweet":model_to_dict(new_retweet),
		"retweet_username":new_retweet.user.username,
		"tweet":{
		"content":tweet.content,
		"username":tweet.user.username,
		"user":tweet.user.id,
		"date_created":tweet.date_created,
		"user_image":tweet.user.profile.image.url,
		},


	})
	


	
def follow_user(request):
	user = get_object_or_404(User,id=request.GET.get('id'))
	followCount = Profile.objects.filter(follow=user).all().count()
	followersCount = user.profile.follow.all().count()
	is_follow = False
	if request.user in user.profile.follow.all():
		user.profile.follow.remove(request.user)
		is_follow = False
	else:
		user.profile.follow.add(request.user)
		is_follow = True
	return JsonResponse({'is_follow':is_follow,
						'followCount':followCount,
						'followersCount':followersCount})




def tweet_detail(request,pk):
	tweet = get_object_or_404(Tweet,pk=pk)
	replies = Reply.objects.filter(tweet=tweet).order_by('-date_reply')

	if request.method == 'POST':
		form = ReplyForm(request.POST)
		if form.is_valid():
			reply = form.save(commit=False)
			reply.tweet = tweet
			reply.user = request.user
			reply.save()
			return HttpResponseRedirect(reverse('tweet-detail',kwargs={'pk': pk}))
	else:
		form = ReplyForm()
	return render(request,'twitterapp/tweet_detail.html',{'tweet':tweet,'replies':replies,'form':form})



class SearcResultsView(generic.ListView):
	model = Profile
	template_name = "twitterapp/search_results.html"
	
	def get_context_data(self,*args,**kwargs):
		context = super().get_context_data(*args,**kwargs)
		context['count'] = self.count or 0
		context['query'] = self.request.GET.get('q')
		return context


	def get_queryset(self):
		request = self.request
		query = request.GET.get('q',None)
		if query is not None:
			tweet_results       = Tweet.objects.search(query)
			profile_results     = Profile.objects.search(query)
            
            # combine querysets 
			queryset_chain = chain(
			        tweet_results,
			        profile_results
			)        
			qs = sorted(queryset_chain, 
			            key=lambda instance: instance.date_created, 
			            reverse=True)
			self.count = len(qs) # since qs is actually a list
			return qs
		return Tweet.objects.none() # just an empty queryset as default




