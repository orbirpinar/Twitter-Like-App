from django.urls import path
from twitterapp import views
from user import views as user_views


urlpatterns = [
		path('home',views.home,name='home'),
		path('',views.landing,name='landing'),
		path('tweet/<int:pk>',views.tweet_detail,name='tweet-detail'),
		path('like/',views.like_tweet,name='like_tweet'),
		path('follow/',views.follow_user,name="follow"),
		path('retweet/',views.retweet,name='retweet'),
		path('search/',views.SearcResultsView.as_view(),name="search-result")
		
		# path('messages/',views.MessageView.as_view(),name='messages'),
		# path('messages/create/<int:user_id>',views.CreateMessageView.as_view(),name="create-message"),
		# path('messages/<int:message_id>',views.MessageDetailView.as_view(),name="message-detail"),
		# path('message/<int:pk>',user_views.UserMessageView.as_view(),name='user-message')

]