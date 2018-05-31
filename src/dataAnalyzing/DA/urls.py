'''

@author: hectorz
'''
import django
from django.conf.urls import url, include
import mysite.settings

from . import views
urlpatterns = [
               url(r'^$', views.index, name='index'),
                url(r'^index',views.index, name='index'),
                url(r'^login',views.login, name='login'),
                url(r'^register',views.register, name='register'),
                url(r'^dsc',include('dsc.urls')),
                url(r'^dsclist\.html',include('dsc.urls')),
                url(r'^db',include('db.urls')),
                url(r'^dblist\.html',include('db.urls')),
               ]
