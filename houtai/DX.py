# # -*- coding: utf-8 -*-
import math
import os

from django.db import connection
from django.http import JsonResponse, HttpResponse
from houtai.models import User, JxZhouqibiao, jx_jixiao, jx_jixiao_all, w_work_info_tmp, j_mission_up
from django.db.models import Q
import xlwt, xlrd
import datetime
from io import BytesIO
import urllib, sys
import urllib.request
import ssl
import time
import json
from new_jx import settings


def handle_upload_file(file, filename):
    path = r'./upload/'  # 图片保存路径
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + filename, 'wb') as destination:
        for chunk in file.chunks():
            # print(chunk)
            destination.write(chunk)
    return filename


def DX_upload(request):
    img_url = ''
    data = {}
    path = ''
    c = []
    data2 = []
    data3 = []
    ht_msg = ''
    # if request.method == "POST":
    img_url = handle_upload_file(request.FILES.get('file'), str(request.FILES['file']))
    msg = {}
    msg['msg'] = '上传成功'
    msg['success'] = True
    msg['path'] = img_url

    path = './upload/' + msg['path']
    #path = './upload/转码前.xlsx'
    data = xlrd.open_workbook(path)
    table = data.sheet_by_name(u'Sheet1')  # 通过名称获取
    nrows = table.nrows

    cursor = connection.cursor()
    # 清空
    # cursor.execute("truncate table dxfj")

    for j in (range(nrows)):
        table.row_values(j)
        qc = ''
        lianjie = ''
        try:
            pinpai=table.row_values(j)[0]

            xinghao=table.row_values(j)[1]
            qianfariqi=table.row_values(j)[2]
            waipingA=table.row_values(j)[3]
            pingmuchicunA=table.row_values(j)[4]
            xiangsuA1=table.row_values(j)[5]
            xiangsuA2=table.row_values(j)[6]
            neipingfanwei=table.row_values(j)[7]
            neipingchicun=table.row_values(j)[8]
            xiangsuB1=table.row_values(j)[9]
            xiangsuB2=table.row_values(j)[10]
            jishenchichun1=table.row_values(j)[11]
            jishenchichun2=table.row_values(j)[12]
            caozuoxitong=table.row_values(j)[13]
            zhinengshuoji=table.row_values(j)[14]
            tupiandizhi=table.row_values(j)[15]
            wangzhi=table.row_values(j)[16]
            #转码
            djxcd=float(pingmuchicunA)*25.4
            djxxs=math.sqrt(float(xiangsuA1)*float(xiangsuA1)+float(xiangsuA2)*float(xiangsuA2))
            xszj=float(djxcd)/float(djxxs)
            pmg=float(xszj)*float(xiangsuA1)
            pmk=float(xszj)*float(xiangsuA2)
            pmmj=float(pmg)*float(pmk)
            sjmj=float(jishenchichun1)*float(jishenchichun2)
            def sprintf(fs,*args):
                s=fs%args*100
                return s
            zspzb=sprintf(pmmj,sjmj)

            cursor.execute(
                "INSERT INTO newdx (pinpai,xinghao,waipingA,pingmuchichunA,caozuoxitong,zongzhi) "
                "VALUES ('{}','{}','{}','{}','{}','{}')".format(
                    pinpai,
                    xinghao,
                    waipingA,
                    pingmuchicunA,
                    caozuoxitong,
                    zspzb,
                ))
            row = cursor.fetchall()
            ht_msg = ''
        except Exception:
            ht_msg = '123'
            break

    cursor1 = connection.cursor()
    cursor1.execute("SELECT * FROM `newdx` order by id asc ")
    list_obj = cursor1.fetchall()

    # 创建工作簿
    wb = xlwt.Workbook(encoding='utf-8')

    sheet = wb.add_sheet('order-sheet')

    # 写入文件标题
    if list_obj:
        # 创建工作薄
        sheet.write(0, 0, u"id")
        sheet.write(0, 1, u"pinpai")
        sheet.write(0, 2, u"xinghao")
        sheet.write(0, 3, u"waipingA")
        sheet.write(0, 4, u"pingmuchicunA")
        sheet.write(0, 5, u"caozuoxitong")
        sheet.write(0, 6, u"zongzhi")
        # 写入数据
        excel_row = 1
        for obj in list_obj:
            sheet.write(excel_row, 0, obj[0])
            sheet.write(excel_row, 1, obj[1])
            sheet.write(excel_row, 2, obj[2])
            sheet.write(excel_row, 3, obj[3])
            sheet.write(excel_row, 4, obj[4])
            sheet.write(excel_row, 5, obj[5])
            sheet.write(excel_row, 6, obj[6])
            count = 0
            excel_row = excel_row + count + 1

            # 检测文件是够存在
        ###########################以下为正确代码
        # os.path.exists判断括号里的文件是否存在的意思，括号内的可以是文件路径。
        exist_file = os.path.exists(r"./upload/电信解码.xls")
        if exist_file:
            os.remove(r"./upload/电信解码.xls")
        wb.save(r"./upload/电信解码.xls")
        # BytesIO操作二进制数据
        sio = BytesIO()
        wb.save(sio)
        # seek()方法用于移动文件读取指针到指定位置
        sio.seek(0)
        response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=./upload/电信解码.xls'
        response.write(sio.getvalue())


    return HttpResponse(ht_msg)
