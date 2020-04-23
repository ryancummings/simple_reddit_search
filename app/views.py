from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import SearchForm

import praw
from datetime import datetime, timedelta
import requests
import json

reddit = praw.Reddit(client_id='o69SO2QHp15j2A',
                     client_secret='yXmkfIVmbwrt3u6T8d8oRDLvOEw',
                     user_agent='test')

def searchReddit(subreddit, terms):
    newPosts = []
    subreddit_instance = reddit.subreddit(subreddit)
    
    for submission in subreddit_instance.new():
        flag = False
        for term in terms:
            if term in submission.title.lower():
                flag = True
        
        if flag == True:
            newPosts.append({
                "id": submission.id,
                "subreddit": subreddit,
                "title": submission.title,
                # "content": submission.selftext,
                "timestamp": datetime.fromtimestamp(submission.created).strftime("%b %d %H:%M:%S"),
                "url": 'http://www.reddit.com' + submission.permalink
            })
    return newPosts
        
def index(request):
    posts = []
    messages = []
    if request.method == 'POST':
        print(request)
        form = SearchForm(request.POST)
        if form.is_valid():
            subreddit = form.cleaned_data['subreddit']
            terms = form.cleaned_data['search_string'].lower().split(',')
            # Strip whitespace with map and inline function
            terms = list(map(lambda term: term.strip(), terms))
            try:
                posts = searchReddit(subreddit, terms)
                if len(posts) == 0:
                    messages.append('No results for your search in most recent ~100 posts')
            except:
                messages.append('Search failed, double check that the subreddit exists')
                
    context = {'form': SearchForm,
               'posts': posts,
               'messages': messages}
    
    return render(request, 'index.html', context)

# Create your views here.
