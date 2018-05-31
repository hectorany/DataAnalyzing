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
  
from django.forms.formsets import formset_factory  
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage  
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
  
from bootstrap_toolkit.widgets import BootstrapUneditableInput  
import ast

from django.views.decorators.csrf import csrf_protect
from DA.models import CustDataSchem, DataBase
from django.utils import timezone
from django.db import connection

import json

@csrf_protect
def update(request):
    data = request.POST
    pk = data['pk']
    CustDataSchem.objects.filter(id = pk).update(name = data['value'])
    return render(request,"DA/dsc.html")

@csrf_protect
def addDsc(request):
    dsc = CustDataSchem.objects.create(db_created = 0)
    data = json.loads(request.POST['data'])
    dsc.owner = "Default"
    dsc.name = "DataSchemaName"+ str(dsc.id)
    schem = '(\n\t'
    contain = ""
    for entry in data:
        contain = contain + entry['name']+ '\t'+entry['type']+','
    contain = contain[:-1]
    li = contain.split(",")
    li.reverse()
    schem = schem+ ",\n\t".join(li) +"\n)"
    dsc.schem = schem
    dsc.save()
    return render(request,"DA/dsc.html")

def remove(request):
    data = request.POST
    pk = data['pk']
    context = {}
    print(pk)
    dsc = CustDataSchem.objects.get(id = pk)
    if( dsc.db_created > 0 ):
        return HttpResponse('The Schema was referenced by DB.');
    else:
        dsc.delete()
    return HttpResponse("Remove Successfully.")

def show(request):
    dsc_list = CustDataSchem.objects.all()
    context = {"dsc_list":dsc_list}
    #if request.method == 'GET':  
    return render(request,'DA/dsclist.html', context)  
    #else:  
    #    form = request.POST  
    #    if form.is_valid():  
    #        pk = request.POST.get('pk', '')  
    #        if pk is not None :  
    #            dsc_list = CustDataSchem.objects.filter(id='pk')
    #            context = {"dsc_list":dsc_list}
    #            return render(request,'DA/dscdetail.html', context) 
    #        else:  
    #            return render(request,'DA/dsclist.html', context) 
    #    else:  
    #        return render(request,'DA/dsclist.html', context) 
def dscJson(request):
    json_data = serializers.serialize("json",CustDataSchem.objects.all())
    return HttpResponse(json_data,content_type="application/json")
