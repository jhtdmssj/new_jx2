# encoding=utf-8

from django.http import JsonResponse
from django.shortcuts import render

from django.db import connection
import time
import os
import xlwt, xlrd
from django.http import HttpResponse
from tqdm import tqdm

import threading
from io import BytesIO
import time

num_progress = 0  # 当前的后台进度值
def handle_upload_file(file, filename):
    path = r'./upload/'  # 图片保存路径
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + filename, 'wb') as destination:
        for chunk in file.chunks():
            # print(chunk)
            destination.write(chunk)
    return filename
def process_data(request):
    global num_progress
    count_js = 0
    if count_js == 0:
        img_url = handle_upload_file(request.FILES.get('file'), str(request.FILES['file']))
        msg = {}
        msg['msg'] = '上传成功'
        msg['success'] = True
        msg['path'] = img_url

        path = './upload/' + msg['path']
        data = xlrd.open_workbook(path)
        table = data.sheet_by_name(u'Sheet1')  # 通过名称获取
        nrows = table.nrows

        cursor = connection.cursor()
        # cursor.execute("truncate table sjfj")

        # 创建工作簿
        wb = xlwt.Workbook(encoding='utf-8')
        sheet = wb.add_sheet('order-sheet')
        # 写入文件标题
        # 创建工作薄
        sheet.write(0, 0, u"条码")
        sheet.write(0, 1, u"描述")
        sheet.write(0, 2, u"品牌")
        sheet.write(0, 3, u"价格")
        sheet.write(0, 4, u"品牌级别")
        sheet.write(0, 5, u"姓名")
        sheet.write(0, 6, u"确认")
        sheet.write(0, 7, u"QC")
        sheet.write(0, 8, u"连接")
        sheet.write(0, 9, u"库")
        # 写入数据
        excel_row = 1
    for j in range(nrows):
        # ... 数据处理业务
        cursor2 = connection.cursor()
        cursor2.execute("SELECT * FROM fj order by id desc")
        raw = cursor2.fetchall()
        for i in raw:
            val = i[1] in table.row_values(j)[1]
            if val == True:
                table.row_values(j)[6] = i[2]
                table.row_values(j)[7] = i[3]
                qc = i[2]
                lianjie = i[3]
                break
            else:
                qc = ''
                lianjie = ''
        str_v = table.row_values(j)[0]
        def pinpaiku(gjz, str_v):
            if str(gjz) == '690' or str(gjz) == '691':
                c = str_v[0:7]
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM pinpaiku where code='" + c + "' order by id desc")
                raw3 = cursor.fetchall()
                d = raw3
            elif str(gjz) == '692' or str(gjz) == '693' or str(gjz) == '694' or str(gjz) == '695' or str(
                    gjz) == '696':
                c = str_v[0:8]
                cursor2 = connection.cursor()
                cursor2.execute("SELECT * FROM pinpaiku where code='" + c + "' order by id desc")
                raw = cursor2.fetchall()
                d = raw
            elif str(gjz) == '697' or str(gjz) == '698' or str(gjz) == '699':
                c = str_v[0:9]
                cursor2 = connection.cursor()
                cursor2.execute("SELECT * FROM pinpaiku where code='" + c + "' order by id desc")
                raw = cursor2.fetchall()
                d = raw
            else:
                c = str_v[0:8]
                cursor2 = connection.cursor()
                cursor2.execute("SELECT * FROM pinpaiku where code='" + c + "' order by id desc")
                raw = cursor2.fetchall()
                d = raw
            return d
        gjz = str_v[0:3]
        pinpai_fj = pinpaiku(gjz, str_v)
        if len(pinpai_fj):
            pinpai_fj = pinpai_fj[0][2]
        else:
            pinpai_fj = ''
        table.row_values(j)
        sheet.write(excel_row, 0, table.row_values(j)[0])
        sheet.write(excel_row, 1, table.row_values(j)[1])
        sheet.write(excel_row, 2, table.row_values(j)[2])
        sheet.write(excel_row, 3, table.row_values(j)[3])
        sheet.write(excel_row, 4, table.row_values(j)[4])
        sheet.write(excel_row, 5, table.row_values(j)[5])
        sheet.write(excel_row, 6, lianjie)
        sheet.write(excel_row, 7, qc)
        sheet.write(excel_row, 8, '')
        sheet.write(excel_row, 9, pinpai_fj)
        count = 0
        excel_row = excel_row + count + 1

        num_progress = j * 100 / nrows  # 更新后台进度值，因为想返回百分数所以乘100
        res = num_progress
    # 检测文件是够存在
    ###########################以下为正确代码
    # os.path.exists判断括号里的文件是否存在的意思，括号内的可以是文件路径。
    exist_file = os.path.exists(r"./upload/数据分解2022.xls")
    if exist_file:
        os.remove(r"./upload/数据分解2022.xls")
    wb.save(r"./upload/数据分解2022.xls")
    # BytesIO操作二进制数据
    sio = BytesIO()
    wb.save(sio)
    # seek()方法用于移动文件读取指针到指定位置
    sio.seek(0)
    response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=./upload/数据分解.xls'
    response.write(sio.getvalue())
    resp=[]
    resp.append(res)
    resp.append(HttpResponse.status_code)

    return JsonResponse(resp, safe=False)
def show_progress(request):
    print('show_progress----------' + str(num_progress))
    return JsonResponse(num_progress, safe=False)
