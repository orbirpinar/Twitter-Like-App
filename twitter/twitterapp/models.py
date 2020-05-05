from django.db import models
from  django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.db.models import Q

from PIL import Image

#searching 

class TweetQuerySet(models.QuerySet):
	def search(self, query=None):
		qs = self
		if query is not None:
			or_lookup = (Q(content__icontains=query)|
						 Q(user__username__icontains=query))
			qs = qs.filter(or_lookup).distinct()

			return qs



class TweetManager(models.Manager):
	def get_queryset(self):
		return TweetQuerySet(self.model, using = self._db)

	def search(self,query=None):
		return self.get_queryset().search(query=query)

class ProfileQuerySet(models.QuerySet):
	def search(self, query=None):
		qs = self
		if query is not None:
			or_lookup = (Q(user__username__icontains=query))
			qs = qs.filter(or_lookup).distinct()

			return qs



class ProfileManager(models.Manager):
	def get_queryset(self):
		return ProfileQuerySet(self.model, using = self._db)

	def search(self,query=None):
		return self.get_queryset().search(query=query)

	

class Post(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	date_created = models.DateTimeField(default=timezone.now)

	class Meta:
		ordering = ['-date_created']



class Tweet(Post):
	content = models.CharField(verbose_name='Tweet',max_length=200)
	image = models.FileField( verbose_name = "",upload_to="tweet_pics",null=True,blank=True)
	likes = models.ManyToManyField(User,related_name='likes',blank=True)

	objects = TweetManager()
	def get_absolute_url(self):
		return reverse('tweet-detail',args=[str(self.pk)])
	def __str__(self):
		return self.content

	def natural_key(self):
		return(self.content,self.likes.all(),self.user.username,self.date_created)

class RetweetModel(Post):
	retweet = models.ForeignKey(Tweet,on_delete=models.CASCADE,related_name="retweets")



	def __str__(self):
		return self.user.username



class Reply(models.Model):
	tweet = models.ForeignKey('Tweet',on_delete=models.CASCADE,related_name='replies')
	content = models.CharField(verbose_name='',max_length=200)
	user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	date_reply = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.content

class Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	image = models.ImageField(default="default.jpg" ,	upload_to="profile_pics",verbose_name="")
	cover_image = models.ImageField(default="default_cover.jpg",upload_to="cover_pics",verbose_name="")
	bio = models.CharField(max_length=160,null=True,blank=True)
	location = models.CharField(max_length=30,null=True,blank=True)
	birth_date = models.DateField(null=True,blank=True)
	follow = models.ManyToManyField(User,related_name="follower")
	date_created = models.DateTimeField(default=timezone.now)

	objects = ProfileManager()
	
	def get_absolute_url(self):
		return reverse('user-detail',args=[str(self.user.username)])

	def __str__(self):
		return f"{self.user.username} Profili"

	def save(self,*args,**kwargs):
		#run to save method parent class
		super().save(*args,**kwargs)
		img = Image.open(self.image.path)
		cover_img = Image.open(self.cover_image.path)
		
		if cover_img.height>800 or cover_img.width>300:
			c_output_size = (800,300)
			cover_img.thumbnail(c_output_size)
			cover_img.save(self.cover_image.path)
		#eğer profile pic genişliği  veya boyu 300 den büyükse onları 300 yap
		if img.height>300 or img.width>300:
			output_size = (300,300)
			img.thumbnail(output_size)
			img.save(self.image.path)



##Signals when create user then create profile_pics
def create_profile(sender, **kwargs):
	if kwargs['created']:
		user_profile = Profile.objects.create(user=kwargs['instance'])
	
post_save.connect(create_profile,sender=User)







