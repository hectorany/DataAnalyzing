'''

@author: hectorz
'''
from django.shortcuts import render_to_response,render,get_object_or_404    
from django.http import HttpResponse, HttpResponseRedirect    
from django.contrib.auth.models import User    
from django.contrib import auth  
from django.contrib import messages  
from django.template.context import RequestContext  
from django.template import loader
import json
from django.forms.formsets import formset_factory  
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage  
  
from bootstrap_toolkit.widgets import BootstrapUneditableInput  
from django.contrib.auth.decorators import login_required 

def getdsc(request):
    rs=[]
    for i in range(5):
        rsp={}
        rsp["name"]="hector"+str(i)
        rsp["stars"]=str(i)
        rsp["fork"]=str(i+10)
        rsp["description"]="as"*i
        rs.append(rsp)
    return HttpResponse("var gridData=" + json.dumps(rs), content_type="application/json")   
    
