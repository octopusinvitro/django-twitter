import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from webapp.forms.tweet_forms import CreateTweetForm
from webapp.models.tweet import Tweet
from webapp.presenters.tweet_presenter import TweetPresenter


def index(request):
    return render(request, 'tweets/index.html', {'tweets': map(TweetPresenter, Tweet.objects.all())})


def new(request):
    form = CreateTweetForm()
    return render(request, 'tweets/new.html', {'form': form})


@login_required
def create(request):
    form = CreateTweetForm(request.POST, request.FILES)
    if not form.is_valid():
        return render(request, 'tweets/new.html', {'form': form})

    tweet = form.save(commit=False)
    tweet.user = request.user
    tweet.save()

    url = reverse('tweets_show', kwargs={'id': tweet.id})
    messages.success(request, f'Success! <a href="{url}">See your tweet</a>.')
    return HttpResponseRedirect('/')


def show(request, id):
    tweet = get_object_or_404(Tweet, pk=id)
    return render(request, 'tweets/show.html', {'presenter': TweetPresenter(tweet)})


@login_required
def likes(request):
    id = json.loads(request.body or '{}').get('id', None) or None
    if id is None:
        return JsonResponse({'error': 'Invalid data'}, status=400)

    tweet = Tweet.objects.filter(pk=int(id)).first()
    if tweet is None:
        return JsonResponse({'error': 'Tweet not found'}, status=404)

    tweet.likes += 1
    tweet.save()
    return JsonResponse({'likes': tweet.likes})
