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
import os
from django.forms.formsets import formset_factory  
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage  
  
from bootstrap_toolkit.widgets import BootstrapUneditableInput  
from django.contrib.auth.decorators import login_required 

from django.views.decorators.csrf import csrf_protect
from django.conf import settings
import nltk
from DA.models import CustDataSchem, DataBase
import dataoperations
from dataoperations.getbuglist import ImportMain
from dataoperations.tables import dboperator
from django.core import serializers
from datetime import datetime
import json
from django.http import JsonResponse

def update(request):
    data = request.POST
    pk = data['pk']
    DataBase.objects.filter(id = pk).update(name = data['value'])
    return render(request,"DA/db.html")

def addDB(dbname, shown, schema,owner,file):
    print(schema)
    print(dbname)
    dsc = CustDataSchem.objects.get(name = schema)
    db = DataBase.objects.create(data_schema = dsc)
    db.name = dbname
    db.shown = shown
    db.owner = owner
    dsc.db_created = dsc.db_created+1
    dsc.save()
    action = dboperator()
    action.createTable(dbname, dsc.schem) 
    db.items = action.initDb(settings.MEDIA_ROOT+"/"+file)
    db.save()

@csrf_protect
def upload(request):
    if request.method=="POST":
        img=request.FILES.get("file",None)
        if img:
            from django.core.files.uploadedfile import TemporaryUploadedFile
            print(img._get_name(),type(img))
            f=open(settings.MEDIA_ROOT+"/"+img.name,"wb")
            for chunck in img.chunks():
                f.write(chunck)
                f.close()
        else:
            if request.POST["shown"] == "":
                shown = False
            else:
                shown = True        
            datafile = request.POST["datafile"]
            print "datafile is ",datafile
            post = request.POST["post"]
            dbname = post[1:post.find('&')]
            dbname = dbname[dbname.find("=")+1:]
            schema = post[post.find('&')+1:]
            schema = schema[schema.find('=')+1:]
            owner = "Default"
            addDB(dbname, shown, schema, owner,datafile.split('\\')[-1])
        return  render(request,"DA/db.html")
    
    '''
    
    return render(request,"DA/db.html")
'''

@csrf_protect
def dbimport(request):
    if request.method=="POST":
        if request.POST["shown1"] == "":
            shown = False
        else:
            shown = True
        host = request.POST["dbhost"]
        databname = request.POST["databname"]
        user = request.POST["user"]
        password = request.POST["password"]
        start = request.POST["start"]
        end = request.POST["end"]
        post = request.POST["post"]
        dbname = post[1:post.find('&')]
        dbname = dbname[dbname.find("=")+1:]
        schema = post[post.find('&')+1:]
        schema = schema[schema.find('=')+1:]
        owner = "Default"
        print host,databname,user,password,start,end,dbname,schema

        dsc = CustDataSchem.objects.get(name = schema)
        db = DataBase.objects.create(data_schema = dsc)
        db.name = dbname
        db.shown = shown
        db.owner = owner
        dsc.db_created = dsc.db_created+1
        dsc.save()
        db.save()
        action = dboperator()
        print "creating table"
        action.createTable(dbname, dsc.schem) 
        ImportMain(start,end,settings.MEDIA_ROOT,host,user,password,databname,dbname)
        sql = "select count(*) from %s;"%dbname;
        db.items = action.searchItems(sql)[0][0]
        db.save()
    return  render(request,"DA/db.html")

def show(request):
    dsc_list = CustDataSchem.objects.all()
    db_list = DataBase.objects.all()
    context = {"dsc_list":dsc_list,"db_list":db_list}
    #if request.method == 'GET':  
    return render(request,'DA/dblist.html', context)
    '''
    if request.method == 'GET':  
        template = loader.get_template('DA/dblist.html') 
        return HttpResponse(template.render({},request))  
    else:  
        form = request.POST  
        if form.is_valid():  
            pk = request.POST.get('pk', '')  
            if pk is not None :  
                template = loader.get_template('DA/dblist.html') 
                return HttpResponse(template.render({"form":form,},request)) 
            else:  
                template = loader.get_template('DA/dblist.html') 
                return HttpResponse(template.render({"form":form, },request)) 
        else:  
            template = loader.get_template('DA/dblist.html') 
            return HttpResponse(template.render({},request))  
            
        '''
def remove(request):
    data = request.POST
    pk = data['pk']
    print(pk)
    db = DataBase.objects.get(id = pk)
    print(db.data_schema)
    dsc = CustDataSchem.objects.get(name = db.data_schema)
    dsc.db_created = dsc.db_created-1
    action = dboperator()
    print action.dropTable( db.name )
    db.delete()
    dsc.save()
    return HttpResponse("Remove Successfully.")

def numbcharts(request):
    template = loader.get_template('DA/createCharts.html')
    dsc = CustDataSchem.objects.get(name = request.GET.get("schema"))
    dbname = request.GET.get("dbname")
    col = dsc.schem[1:-1]
    db_list = DataBase.objects.all()
    items = [x.split()[0] for x in col.split(',')]
    return HttpResponse(template.render({"schema":dsc.name,"dbname":dbname,"items":items,"db_list":db_list},request))

def getnumbers(request):
    data = []
    drilldowns = []
    resp = {}
    sql = "select %s, count(*) as cnt from %s "
    if request.GET.get("dbname") and request.GET.get("column1"):
        dbname = request.GET.get("dbname")
        column1 = request.GET.get("column1")
        sql = sql %(column1, dbname)+ "group by %s " %column1+" order by cnt desc "
        if request.GET.get("min"):
            min = int(request.GET.get("min"))
            sql = sql +"limit %d" % min
        if request.GET.get("max"):
            max = int(request.GET.get("max"))
            sql = sql +",%d"%(max - min)
        action = dboperator()
        rawdata = action.searchItems(sql)
        flag = True
        for entry in rawdata:
            de = {}
            if entry[0]:
                de['name']=entry[0]
            else:
                de['name']="NONE"
            de["y"]=entry[1]
            de["drilldown"]=de['name']
            data.append(de)
        
        if request.GET.get("column2"):
            column2 = request.GET.get("column2")
            
            for col1 in data:
                sql = "select %s, count(*) as cnt from %s "
                sql = sql %(column2, dbname)
                sql2 = "group by %s " %column2+" order by cnt desc "
                if col1["name"]!= 'NONE':
                    sql = sql + "where %s like '"%column1+col1["name"] +"' "
                else:
                    sql = sql + "where %s='"%column1+"' "
                sql = sql+sql2
                #print(sql)
                rawdata = action.searchItems(sql)
                dri = {}
                dri["name"]=col1["name"]
                dri["id"]=col1["name"]
                
                dri["data"]=[[x,y] for x , y in rawdata]
                drilldowns.append(dri) 
    resp["data"] = data
    resp["drilldowns"] = drilldowns           
    return JsonResponse(resp, safe=False)
    
                    
def timeline(request):
    dsc = CustDataSchem.objects.get(name = request.GET.get("schema"))
    dbname = request.GET.get("dbname")
    col = dsc.schem[1:-1]
    db_list = DataBase.objects.all()
    template = loader.get_template('DA/timeline.html') 
    items = [x.split()[0] for x in col.split(',')]
    return HttpResponse(template.render({"schema":dsc.name,"dbname":dbname,"items":items,"db_list":db_list},request)) 
def timelineShow(request):
    dsc = CustDataSchem.objects.get(name = request.GET.get("schema"))
    dbname = request.GET.get("dbname")
    col = dsc.schem[1:-1]
    db_list = DataBase.objects.all()
    template = loader.get_template('DA/timeline2.html') 
    items = [x.split()[0] for x in col.split(',')]
    sql="select DATE_FORMAT(%s,'%%Y-%%m-%%d'), count(*) from %s " %(request.GET.get("timed"), dbname)
    co = 0
    for item in items:
        if request.GET.get(item+"_con") :
            if co == 0:
                co = 1
                sql = sql + "where "+item+" "+ request.GET.get(item+"_con")+" "
            else:
                sql = sql + " and "+item+" "+ request.GET.get(item+"_con")+" "
    sql = sql + " group by %s "%request.GET.get("timed")
    print(sql)
    action = dboperator()
    data = action.searchItems(sql)
    rsp = []
    for entry in data:
        y,m,d = entry[0].split("-")
        datetime =(int(y),int(m),int(d))
        rsp.append([datetime,entry[1]])
    #json_data = serializers.serialize("json",data)
    return HttpResponse(template.render({"data":json.dumps(rsp)},request))

def keyworkds(request):
    dsc = CustDataSchem.objects.get(name = request.GET.get("schema"))
    dbname = request.GET.get("dbname")
    col = dsc.schem[1:-1]
    db_list = DataBase.objects.all()
    template = loader.get_template('DA/keywords.html') 
    items = [x.split()[0] for x in col.split(',')]
    return HttpResponse(template.render({"schema":dsc.name,"dbname":dbname,"items":items,"db_list":db_list},request)) 

def getKeywords(request):
    dsc = CustDataSchem.objects.get(name = request.GET.get("schema"))
    dbname = request.GET.get("dbname")
    col = dsc.schem[1:-1]
    db_list = DataBase.objects.all()
    items = [x.split()[0] for x in col.split(',')]
    sql="select %s from %s " %(request.GET.get("text"), dbname)
    co = 0
    for item in items:
        if request.GET.get(item+"_con") :
            if co == 0:
                co = 1
                sql = sql + "where "+item+" "+ request.GET.get(item+"_con")+" "
            else:
                sql = sql + " and "+item+" "+ request.GET.get(item+"_con")+" "
    #sql = sql + " group by %s "%request.GET.get("timed")
    #print(sql)
    action = dboperator()
    data = action.searchItems(sql)
    strset = ''
    for entry in data:
        strset = strset + entry[0]
    #json_data = serializers.serialize("json",data)
    text = makeText(strset)
    keyfreq = getKeyFreq(text)
    colloc = getColloctions(text)
    kword = '''
         <span class="label label-info">%s    <span class="badge">%d</span></span>
    '''
    htm = " <h5>Frequent Words</h5> "
    if len(keyfreq) == 0:
        htm = htm + "<span class='label label-warning'>Not found</span>"
    else:
        for word in keyfreq:
            if word[0] != ',' and word[0] != '.'  and word[0] != ':':
                htm = htm + kword% word
    htm = htm +" <h5>Colloctions</h5> "
    collocat = '''
        <span class="label label-primary">%s</span>
    '''
    print(colloc)
    if len(colloc) == 0:
        htm = htm + "<span class='label label-warning'>Not found</span>"
    else:
        for entry in colloc.split(";"):
            htm = htm + collocat %entry
    return HttpResponse(htm)
    #return HttpResponse(sql)
def makeText(text):
    tokens = nltk.word_tokenize(text)
    return nltk.Text(tokens)

def getKeyFreq(text,num=30):
    fdist = nltk.FreqDist(text)
    return fdist.most_common(num)

def getColloctions(text,num=50):
    return text.collocations(num=num)
