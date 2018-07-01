"""Evite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from event import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('signup/', views.signup, name='signup'),
    url('login/', auth_views.login, name='login'),
    url('logout/', auth_views.logout, name='logout'),
    url('event/', views.event, name='event'),
    url('add/', views.add, name='add'),
    url('details/(?P<pk>[0-9]+)/$', views.details, name='details'),
    url('send/(?P<eventid>[0-9]+)/$', views.send, name='send'),
    url('delete/(?P<eventid>[0-9]+)/$', views.delete, name='delete'),
    url('edit/(?P<eventid>[0-9]+)/$', views.edit, name='edit'),
    url('sendr/(?P<eventid>[0-9]+)/$', views.sendr, name='sendr'),
    url(r'^rsvp/(?P<guid>[0-9A-Za-z_\-]+)/',views.rsvp, name='rsvp'),
    url(r'^feedback/(?P<guid>[0-9A-Za-z_\-]+)/',views.feedback, name='feedback'),
]
