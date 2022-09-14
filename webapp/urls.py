"""django_twitter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import path
from django.views.static import serve

from .views import tweets
from .views import users

urlpatterns = [
    path('', tweets.index, name='tweets_index'),
    path('tweets/new', tweets.new, name='tweets_new'),
    path('tweets', tweets.create, name='tweets_create'),
    path('tweets/<int:id>', tweets.show, name='tweets_show'),
    path('tweets/likes', tweets.likes, name='tweets_likes'),

    path('users/login', users.sign_in, name='users_login'),
    path('users/authentication', users.authentication, name='users_authentication'),
    path('users/logout', users.sign_out, name='users_logout'),

    path('users/new', users.new, name='users_new'),
    path('users', users.create, name='users_create'),
    path('users/edit', users.edit, name='users_edit'),
    path('users/<int:id>', users.update, name='users_update'),
    path('users/<str:username>', users.show, name='users_show'),
]

if settings.DEBUG:
    urlpatterns += [
        path(f'{settings.MEDIA_URL[1:]}<path:path>', serve, {'document_root': settings.MEDIA_ROOT})
    ]
