from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.translation import gettext as _

from webapp.forms.user_forms import CreateUserForm, LoginUserForm, UpdateUserForm
from webapp.models.tweet import Tweet
from webapp.presenters.tweet_presenter import TweetPresenter


def new(request):
    form = CreateUserForm()
    return render(request, 'users/new.html', {'form': form, 'action': reverse('users_create')})


def create(request):
    form = CreateUserForm(request.POST, request.FILES)
    if not form.is_valid():
        return render(request, 'users/new.html', {'form': form, 'action': reverse('users_create')})

    form.save(commit=True)
    messages.success(request, _('join_success_message'))
    return HttpResponseRedirect(reverse('users_login'))


def show(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    tweets = Tweet.objects.filter(user=user)
    return render(request, 'users/show.html', {'user': user, 'tweets': map(TweetPresenter, tweets)})


def edit(request):
    form = UpdateUserForm(instance=request.user)
    action = reverse('users_update', kwargs={'id': request.user.id})
    return render(request, 'users/edit.html', {'form': form, 'action': action})


@login_required
def update(request, id):
    if id != request.user.id:
        messages.error(request, 'Current user can not update this user')
        return HttpResponseRedirect(reverse('users_edit'))

    form = UpdateUserForm(instance=request.user, data=request.POST, files=request.FILES)
    if not form.is_valid():
        action = reverse('users_update', kwargs={'id': request.user.id})
        return render(request, 'users/edit.html', {'form': form, 'action': action})

    form.save(commit=True)
    messages.success(request, 'Details were updated.')
    return HttpResponseRedirect(reverse('users_show', kwargs={'username': request.user.username}))


def sign_in(request):
    form = LoginUserForm()
    return render(request, 'users/login.html', {'form': form})


def authentication(request):
    form = LoginUserForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'users/login.html', {'form': form})

    username = form.cleaned_data['username']
    password = form.cleaned_data['password']
    user = authenticate(username=username, password=password)
    if user is None or not user.is_active:
        messages.error(request, 'Incorrect login credentials.')
        return render(request, 'users/login.html', {'form': form})

    login(request, user)
    return HttpResponseRedirect('/')


def sign_out(request):
    logout(request)
    return HttpResponseRedirect('/')
