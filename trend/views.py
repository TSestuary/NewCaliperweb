# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from task.models import Task

# Create your views here.
def trend(request):
    tasks = Task.objects.all().order_by("-id")
    return render(request, 'trend.html',{'tasks':tasks})