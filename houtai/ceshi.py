# # -*- coding: utf-8 -*-
import os
import json
from django.http import JsonResponse, HttpResponse
from django.db import connection
def testcs(request):
    try:
        data={}
        # 基础表
        ar={}
        arr=[]
        cursor1 = connection.cursor()
        cursor1.execute("SELECT DISTINCT(dl) FROM 2021tubiao_kehu ")
        raw = cursor1.fetchall()  # 读取所有
        for v in (raw):
            cursor2 = connection.cursor()
            cursor2.execute("SELECT DISTINCT(xl) FROM 2021tubiao_kehu where dl='"+v[0]+"'")
            raw2=cursor2.fetchall()
            arr2=[]
            for k in (raw2):
                arr2.append(k[0])
                cursor3 = connection.cursor()
                cursor3.execute("SELECT DISTINCT(pp) FROM 2021tubiao_kehu where dl='" + v[0] + "' and  xl='" + k[0] + "'")
                raw3 = cursor3.fetchall()
                arr3 = []
                for n in (raw3):
                    arr3.append({"name":n[0]})
                arr2.append({"name":k[0],"children":arr3})
            arr.append({"name":v[0],"children":arr2})
        ar={"name":"list","children":arr}

        connection.commit()
        connection.close()
    except Exception as e:
        connection.rollback()
        connection.close()
    #家sdafe=False 避免报错
    return JsonResponse(ar, safe=False)
