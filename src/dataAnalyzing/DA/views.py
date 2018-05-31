# Create your views here.
from django.shortcuts import render_to_response,render,get_object_or_404    
from django.http import HttpResponse, HttpResponseRedirect    
from django.contrib.auth.models import User    
from django.contrib import auth  
from django.contrib import messages  
from django.template.context import RequestContext  
from django.template import loader
  
from django.forms.formsets import formset_factory  
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage  
  
from bootstrap_toolkit.widgets import BootstrapUneditableInput  
from django.contrib.auth.decorators import login_required  
from DA.models import CustDataSchem, DataBase
from .forms import LoginForm  

def index(request):
    login_already=True
    user_name="HectorZ"
    dsc_list = CustDataSchem.objects.all()
    db_list = DataBase.objects.all()
    template = loader.get_template('DA/index.html') 
    return HttpResponse(template.render({"login_already":login_already,"user_name":user_name,"dsc_list":dsc_list,"db_list":db_list},request))  

def register(request):
    template = loader.get_template('DA/register.html') 
    return HttpResponse(template.render({},request))  
 
def login(request):  
    if request.method == 'GET':  
        form = LoginForm()
        template = loader.get_template('DA/login.html') 
        return HttpResponse(template.render({"form":form},request))  
    else:  
        form = LoginForm(request.POST)  
        if form.is_valid():  
            username = request.POST.get('username', '')  
            password = request.POST.get('password', '')  
            user = auth.authenticate(username=username, password=password)  
            if user is not None and user.is_active:  
                auth.login(request, user)  
                template = loader.get_template('DA/index.html') 
                return HttpResponse(template.render({"form":form,},request)) 
            else:  
                template = loader.get_template('DA/login.html') 
                return HttpResponse(template.render({"form":form, 'password_is_wrong':True,},request)) 
                  
        else:  
            template = loader.get_template('DA/login.html') 
            return HttpResponse(template.render({"form":form, },request)) 