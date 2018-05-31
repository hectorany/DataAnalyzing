'''

@author: hectorz
'''
import django
from django.conf.urls import url, include
import mysite.settings

from . import views
urlpatterns = [
                url(r'dsc',views.getdsc, name='getdsc'),

               ]
