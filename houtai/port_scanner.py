# # -*- coding: utf-8 -*-
import os

from django.db import connection
from django.http import JsonResponse, HttpResponse
import xlwt, xlrd
from io import BytesIO

from xlutils.copy import copy
def base_dir(filename=None):
    return os.path.join(os.path.dirname(__file__),filename)

# 导入需要读取Excel表格的路径


# 将excel表格内容导入到tables列表中
def import_excel():
    data = xlrd.open_workbook(r'C:\Users\jihongtao\Desktop\新建文件夹\\duibi.xlsx')
    table = data.sheets()[0]

    wb = copy(data)
    sheet = wb.get_sheet(0)
    for rown in range(table.nrows):
        array = {'tiaoma': '', 'tiaoma_dy': '', 'maioshu': ''}
        array['tiaoma'] = table.cell_value(rown, 1)
        array['tiaoma_dy'] = table.cell_value(rown, 2)
        array['miaoshu'] = table.cell_value(rown, 4)
        # 将Excel表格中的时间格式转化
        myName = "不包含"
        if myName in array['miaoshu']:
            sheet.write(rown,4,'无')
    wb.save('duibi.xlsx')

if __name__ == "__main__":
    # 将excel表格的内容导入到列表中
    import_excel()
    # 验证Excel文件存储到列表中的数据

