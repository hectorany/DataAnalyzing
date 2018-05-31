'''

@author: hectorz
'''
import django
from django.conf.urls import url, include
import mysite.settings

from . import views
urlpatterns = [
                url(r'^$', views.show, name='show'),
                url(r'^addDsc',views.addDsc, name='addDsc'),
                url(r'^update',views.update, name='update'),
                url(r'^remove',views.remove, name='remove'),
                url(r'^dscjson',views.dscJson, name='dscjson'),
               ]
