# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals
import datetime 
from datetime import date
from django.utils import timezone
from ttp import ttp
from datetime import timedelta

from django.db import models

class Tweets(models.Model):
    tweet_id = models.IntegerField(primary_key=True)
    twitter_tweet_id = models.CharField(max_length=200, blank=True)
    text = models.CharField(max_length=300, blank=True)
    user = models.CharField(max_length=200, blank=True)
    date = models.CharField(max_length=100, blank=True)
    class Meta:
        db_table = 'tweets'

    def __unicode__(self):
        return self.user + ' : ' + self.text

    def is_today(self):
        return date.fromtimestamp(self.date/1000.0) >  date.today() - timedelta(days=1)
    
    def text_as_html(self):
        p = ttp.Parser()
        result = p.parse(self.text)
        return result.html

    def hashtags(self):
        p = ttp.Parser()
        result = p.parse(self.text)
        hashlist = result.tags;
        l = list()
        for f in hashlist:
            l.append(str("#"+f))
        return l

class User(models.Model):
    username = models.CharField(max_length=50, blank=False)
    profilepicture = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=500, blank=True)
    language = models.CharField(max_length=100, blank=True)
    url = models.CharField(max_length=300, blank=True)
    fav_count = models.IntegerField(blank=True)
    followers_count = models.IntegerField(blank=True)
    friends_count = models.IntegerField(blank=True)
    date_created = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'users'

    def __unicode__(self):
        return str(self.username)

class Search(models.Model):
    searchtext = models.CharField(max_length=200, blank=False)
    searchdate = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'searches'

    def __unicode__(self):
        return str(self.searchtext)
