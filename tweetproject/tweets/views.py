from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import time
from time import mktime
from datetime import timedelta
from datetime import date
from ttp import ttp
import collections

from tweets.models import Tweets, User, Search

# Create your views here.

def index(request):
    latest_tweets_list = Tweets.objects.all().order_by('-date')[:8]

#    date = datetime.date.today()
 #   start_week = date - datetime.timedelta(date.weekday())
  #  end_week = start_week + datetime.timedelta(7)
   # entries = Tweets.objects.filter(created_at__range=[start_week, end_week])latest_tweets_list

    today = datetime.date.today()
    today = today - datetime.timedelta(days=today.weekday())
    this_weeks_tweets = Tweets.objects.filter(date__gte=int(time.mktime(today.timetuple())*1000))

    last_five_searches = Search.objects.all().order_by('-searchdate')[:5]
    
    most_common = find_most_tweeter(this_weeks_tweets)
    
    chart_array = loop_through_week(this_weeks_tweets)
    
    context = {'latest_tweets_list': latest_tweets_list, 'chart_array': chart_array, 'amount_of_tweets': len(Tweets.objects.all()), 'most_common': most_common, 'searches': last_five_searches}
    return render(request, 'tweets/index.html', context)

def search(request):
    person_filter_term = request.GET.get('personfilter');
    search_term = request.GET.get('search_term')

    results = Tweets.objects.all()

    search = Search(searchtext=search_term).save()

    if search_term is not None and search_term != '':
        results = results.filter(text__icontains=search_term)
    
    if person_filter_term is not None and person_filter_term != '':
        results = results.filter(user=person_filter_term)
    
    # unique_users = results.values_list('user', flat=True);
    unique_users = User.objects.all();

    search_size = len(results)

    paginator = Paginator(results, 15)

    page = request.GET.get('page')
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        results = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        results = paginator.page(paginator.num_pages)

    context = {'results': results, 'search_term': search_term, 'usernames': set(unique_users), 'amount_of_tweets': len(Tweets.objects.all()), 'search_size': search_size}
    return render(request, 'tweets/search/result.html', context)

def user(request, username):

    result = User.objects.all().filter(username=username)
    
    results  = Tweets.objects.all().filter(user=username).order_by('-date')
    paginator = Paginator(results, 10)

    page = request.GET.get('page')
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        results = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        results = paginator.page(paginator.num_pages)

    today = datetime.date.today()
    today = today - datetime.timedelta(days=today.weekday())
    this_weeks_tweets = Tweets.objects.filter(user=username).filter(date__gte=int(time.mktime(today.timetuple())*1000))
    chart_array = loop_through_week(this_weeks_tweets)

    context = {'results': results, 'result': result.get(), 'username': username, 'latest_tweets_list': results, 'chart_array': chart_array}
    return render(request, 'tweets/user/user.html', context)
    

def loop_through_week(tweet_list):
    count = 0
    my_list = list()
    today = date.today()
    for x in range(0, 7):
        offset = (today.weekday() - x) %7
        last_day = today - timedelta(days=offset)
        # print last_day
        for o in tweet_list:
            if date.fromtimestamp(o.date/1000.0) == last_day:
                count = count + 1
        my_list.append(count)
        count = 0
    return my_list
    
def find_most_tweeter(tweet_list):
    users = tweet_list.values_list('user', flat=True)
    counter = collections.Counter(users)
    return counter.most_common()
