from django.contrib import admin
from tweets.models import Tweets

class TweetsAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'twitter_tweet_id')
    list_filter = ['user']
    search_fields = ['text']

# Register your models here.
admin.site.register(Tweets, TweetsAdmin)
