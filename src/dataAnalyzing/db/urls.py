'''

@author: hectorz
'''
import django
from django.conf.urls import url, include
import mysite.settings

from . import views
urlpatterns = [
                url(r'^$', views.show, name='show'),
                url(r'^update',views.update, name='update'),
                url(r'^upload',views.upload, name='upload'),
                url(r'^remove',views.remove, name='remove'),
                url(r'^import',views.dbimport, name='import'),
                url(r'^numbcharts',views.numbcharts, name='numbcharts'),
                url(r'^timeline$',views.timeline, name='timeline'),
                url(r'^timeShow',views.timelineShow, name='timelineShow'),
                url(r'^getnumbers',views.getnumbers, name='getnumbers'),
                url(r'^keywords',views.keyworkds, name='keyworkds'),
                url(r'^getkeywords',views.getKeywords, name='getKeyworkds'),
               ]
