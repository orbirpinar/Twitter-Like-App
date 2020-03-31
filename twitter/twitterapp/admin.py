from django.contrib import admin

from .models import Profile, Tweet,Reply,RetweetModel

class TweetAdmin(admin.ModelAdmin):
	list_display = ('user','content')


admin.site.register(Tweet,TweetAdmin)
admin.site.register(Profile)
admin.site.register(Reply)
admin.site.register(RetweetModel)




