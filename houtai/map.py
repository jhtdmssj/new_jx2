# # -*- coding: utf-8 -*-
import os
import json
from django.http import JsonResponse, HttpResponse
from django.db import connection
def map_zuobiao_list(request):
    data = {}
    c = []
    cursor1 = connection.cursor()
    cursor1.execute("select * from map")
    raw = cursor1.fetchall()  # 读取所有
    for ar in raw:
        c.append({
             "id":ar[0],
             "x":str(ar[1]),
             "y":str(ar[2]),
        })
    data['list'] = (list(c))

    return JsonResponse(data)

def map_list_del2(request):
    x = str(request.GET.get('xx'))
    y = str(request.GET.get('yy'))
    print(x)

    cursor2 = connection.cursor()
    cursor2.execute("delete FROM map WHERE x ='"+x+"' and y ='"+y+"' ")
    raw = cursor2.fetchall()  # 读取所有
    return HttpResponse()




def map_list_del(request):
    name = str(request.GET.get('name'))
    cursor1 = connection.cursor()
    cursor1.execute("CREATE TABLE temp(SELECT `name` FROM map WHERE name = '"+name+"')")
    raw = cursor1.fetchall()  # 读取所有

    cursor2 = connection.cursor()
    cursor2.execute("delete FROM map WHERE name ='"+name+"'")
    raw = cursor2.fetchall()  # 读取所有

    cursor3 = connection.cursor()
    cursor3.execute("drop  table temp")
    raw = cursor3.fetchall()  # 读取所有


    return HttpResponse()

def map_list(request):
    data = {}
    c=[]
    cursor1 = connection.cursor()
    name = request.GET.get('name')
    cursor1.execute("SELECT name,x,y,id FROM `map`")
    raw = cursor1.fetchall()  # 读取所有
    for ar in raw:
        c.append({
            'name': str(ar[0]),
            'x': str(ar[1]),
            'y': str(ar[2]),
            'id': str(ar[3]),
        })

    data['list'] = (list(c))

    return JsonResponse(data)


def map_list2(request):
    data = {}
    c=[]
    cursor1 = connection.cursor()
    cursor1.execute("SELECT DISTINCT(name) FROM `map`")
    raw = cursor1.fetchall()  # 读取所有
    for ar in raw:
        c.append({
            'name': str(ar[0]),
        })

    data['list'] = (list(c))

    return JsonResponse(data)

def map_zb(request):
    if (request.GET.get('xzb')):
        xzb = (request.GET.get('xzb'))
    else:
        xzb = 116
    if (request.GET.get('yzb')):
        yzb = (request.GET.get('yzb'))
    else:
        yzb = 34

    if (request.GET.get('hshu')):
        hshu = (request.GET.get('hshu'))
    else:
        hshu = 9
    if (request.GET.get('zshu')):
        zshu = (request.GET.get('zshu'))
    else:
        zshu = 5

    x = (float(xzb))
    y = (float(yzb))
    chazhi = 0.032
    chazhi2 = 0.025

    jh = []
    jh2 = []
    jh_x = []
    jh_y = []
    hx = []
    sx = []
    for dw in range(int(hshu)):
        wz = round(x - chazhi * dw, 6)
        jh_x.append(wz)
    for dw in range(int(hshu)):
        wz = round(x + chazhi * dw, 6)
        jh_x.insert(0, wz)
    jh_x = sorted(set(jh_x), key=jh_x.index)

    for dw in range(int(zshu)):
        wz = round(y - chazhi2 * dw, 6)
        jh_y.append(wz)

    for dw in range(int(zshu)):
        wz = round(y + chazhi2 * dw, 6)
        jh_y.insert(0, wz)
    jh_y = sorted(set(jh_y), key=jh_y.index)

    for ind, j in enumerate(jh_y):
        for index, i in enumerate(jh_x):
            jh.append({"x": jh_x[index], "y": jh_y[ind]})
    data = {}
    data['list'] = (list(jh))
    cursor1 = connection.cursor()
    name = request.GET.get('name')
    for index, v in enumerate(jh):
        cursor1.execute("INSERT INTO  map (x,y,name) VALUES('" + str(jh[index]["x"]) + "','" + str(
            jh[index]["y"]) + "','" + name + "')")
        raw = cursor1.fetchall()  # 读取所有

    return JsonResponse(data, safe=False)
