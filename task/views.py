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

# Create your views here.
def home(request):
    tasks = Task.objects.all().order_by(OrderBy(RawSQL("cast(results->%s->%s->>%s as float)", ("Performance","algorithm","Total_Scores")), descending=True))
    return render(request,'home.html',{'tasks':tasks})


