# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import json
import time
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from models import Task
from django.db.models.expressions import RawSQL, OrderBy
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import StreamingHttpResponse
from login.views import file_iterator
import tarfile

# Create your views here.
UPLOAD_PATH = settings.UPLOAD_PATH

def home(request):
    # tasks = Task.objects.all().order_by(OrderBy(RawSQL("cast(results->%s->%s->>%s as float)", ("Performance","algorithm","Total_Scores")), descending=True))
    tasks = Task.objects.all().order_by("-id")
    return render(request,'home.html',{'tasks':tasks})

def result(request,taskid):
    task = Task.objects.get(id=taskid)
    output_path = task.output_path
    dirs = os.path.dirname(output_path)
    untar_dirs = output_path.replace(".tar.gz", "")
    if os.path.isdir(untar_dirs):
        pass
    else:
        t = tarfile.open(output_path)
        t.extractall(path = dirs)
    result_files = showtree(os.path.join(untar_dirs,"output"))
    return render(request,'result.html',{'result_files':json.dumps(result_files)}) 
    # return render(request,'result.html')

def result_Download(request,output_path):
    download_name = os.path.basename(output_path)
    response = StreamingHttpResponse(file_iterator(output_path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(download_name)
    return response

def showtree(rootDir): 
    # result_dirs=[]
    result_files=[]
    list_dirs = os.walk(rootDir) 
    for root, dirs, files in list_dirs: 
        '''
        for d in dirs: 
            dirpath=os.path.join(root, d)
            result_dirs.append(dirpath.split("output\\")[1])    
        '''
        for f in files: 
            filepath=os.path.join(root, f)  
            result_files.append(filepath)
    return result_files

def ajax_showresult(request):
    resultpath=request.POST['resultpath']
    file=open(resultpath)
    filecontent= file.read()
    file.close()
    return HttpResponse(filecontent)

@csrf_exempt 
def test_post(request):
    if "file" in request.FILES:
        file = request.FILES['file']
        filename = str(request.FILES['file'])
        if not os.path.exists(UPLOAD_PATH):
            os.mkdir(UPLOAD_PATH)
        save_path = os.path.join(UPLOAD_PATH ,filename.decode('utf-8'))
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
    return HttpResponse(save_path)

@csrf_exempt 
def save_data(request):
    save_path = request.POST['save_path']
    json_data = eval(request.POST['json_data'])
    task = Task(name=json_data['name'])
    task.configuration = json_data['Configuration']
    task.results = json_data['results']
    task.output_path = save_path
    task.save()
    return HttpResponse(task.id)


