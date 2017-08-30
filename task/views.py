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

# Create your views here.
UPLOAD_PATH = settings.UPLOAD_PATH

def home(request):
    tasks = Task.objects.all().order_by(OrderBy(RawSQL("cast(results->%s->%s->>%s as float)", ("Performance","algorithm","Total_Scores")), descending=True))
    return render(request,'home.html',{'tasks':tasks})

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


