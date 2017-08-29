# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.shortcuts import render
from collections import OrderedDict
from task.models import Task

TOTAL_STR = 'Total_Scores'
POINT_STR = 'Point_Scores'
PERF_STR = 'Performance'
FUNC_STR = 'Functional'

# Create your views here.
def compare(request):
    platform_multi_select = request.POST.getlist('platform_multi_select')
    # tasks = Task.objects.all()
    tasks = Task.objects.filter(name__in=platform_multi_select)
    task_num = tasks.count()
    dic_total = {}
    dic_sum = get_sum_dics(tasks)
    dic_total['dic_sum'] = json.dumps(dic_sum)
    for key in dic_sum.keys():
        if dic_sum[key]:
            key = _deal_keyword(key)
            dic_total[key] = True 
    dic_total['platforms'] = platform_multi_select
    return render(request, 'compare.html',dic_total)

def test_aspect(request,aspect):
    tasks = Task.objects.all().order_by("id")
    task_num = tasks.count()
    dic_total = {}
    test_point=[]
    dic_aspect = get_detail_data(tasks, PERF_STR, aspect)   
    dic_total['dic_aspect'] = json.dumps(dic_aspect)
    for key in dic_aspect.keys():
        # key_name = _deal_keyword(key)
        # dic_total[key_name] = True
        test_point.append(key)
    test_point=sorted(test_point)
    dic_total['aspect']=aspect 
    return render(request, 'test_aspect.html', {'dic_total':dic_total,'test_point':test_point})

def select(request):
    tasks = Task.objects.all()
    return render(request, 'select.html',{'tasks':tasks})

def get_sum_dics(tasks):
    dic = {}
    dic['config'] = {}
    dic['test_tools'] = {}
    dic['summary'] = {}

    conf_tmp = OrderedDict()
    for task in tasks:
        target = task.name
        conf_tmp[target] = task.configuration
    dic['config'] = conf_tmp
    dic['perf_summary'] = get_eachItem_sum(tasks, PERF_STR)
    dic['func_summary'] = get_eachItem_sum(tasks, FUNC_STR)
    return dic

def get_eachItem_sum(tasks, testItem):

    summary_tmp = OrderedDict()
    for task in tasks:
        target = task.name
        sum_tmp = {}
        if testItem in task.results.keys():
            sum_dic = task.results[testItem]
        else:
            return {}
        for key in sum_dic.keys():
            sum_tmp[key] = sum_dic[key][TOTAL_STR]
        summary_tmp[target] = sum_tmp
    return summary_tmp

def get_detail_data(tasks, testItem, category):
    dic = {}
    dic['sum'] = get_each_sum_item(tasks, testItem, category)
    for task in tasks:
        try:
            perf_dic = task.results[testItem][category]
            for key in perf_dic.keys():
                if (key != TOTAL_STR):
                    dic[key] = {}
            break
        except Exception:
            dic = {}
    for key in dic.keys():
        if (key == TOTAL_STR or key == 'sum'):
            continue
        tmp_dic = OrderedDict()
        order_dicts = OrderedDict()
        for task in tasks:
            target = task.name
            try:
                test_points = task.results[testItem][category][key]
                tmp_dic[target] = test_points[POINT_STR]
            except Exception:
                test_points = {}
                tmp_dic[target] = 0
            order_list= sorted(tmp_dic[target].iteritems(), key=lambda d:d[0])
            order_dic = OrderedDict()
            for item in order_list:
                order_dic[item[0]] = item[1]
            order_dicts[target]=order_dic
        dic[key] = order_dicts
    return dic

def get_each_sum_item(tasks, testItem, category):
    dic = OrderedDict()
    for task in tasks:
        tmp_dic = OrderedDict()
        target = task.name
        dic[target] = OrderedDict()
        try:
            perf_dic = task.results[testItem][category]
            for key in perf_dic.keys():
                if (key != TOTAL_STR):
                    tmp_dic[key] = perf_dic[key][TOTAL_STR]
        except Exception:
            tmp_dic = {}
        order_list= sorted(tmp_dic.iteritems(), key=lambda d:d[0])
        order_dic = OrderedDict()
        for item in order_list:
            order_dic[item[0]] = item[1]
        dic[target] = order_dic
    return dic

def _deal_keyword(string):
    new_str = '_'.join(string.split('/'))
    new_str = '_'.join(new_str.split(' '))
    new_str = '_'.join(new_str.split('-'))
    return new_str