import os

from django.contrib.sites import requests
from django.db import connection
from django.http import JsonResponse, HttpResponse
from houtai.models import User, JxZhouqibiao, jx_jixiao, jx_jixiao_all, w_work_info_tmp, j_mission_up
from django.db.models import Q
import xlwt, xlrd
import datetime
from io import BytesIO
import time
import json
import requests
from new_jx import settings
def test_kd(request):
    # 需要安装：  pip install requests
    # 以下需要修改
    appcode = "1fb56623de844f1bb2de46c28a2db5cf"
    req_data = {
        'com': 'zhongtong',
        'nu': '75450632975559',
        'receiverPhone': '',
        'senderPhone': ''
    }
    # 修改结束

    url = "http://ali-deliver.showapi.com/showapi_expInfo"
    headers = {
        'Authorization': 'APPCODE ' + appcode
    }

    try:
        html = requests.get(url, headers=headers, data=req_data)
    except:
        print("URL错误")
        exit()
    print("---------response status is:-------------")
    print(html.status_code)
    print("---------response headers are:-------------")
    print(html.headers)
    msg = html.headers.get('X-Ca-Error-Message')
    status = html.status_code


    if status == 200:
        print("status为200，请求成功，计费1次。（status非200时都不计费）")
    else:
        if (status == 400 and msg == 'Invalid AppCode'):
            print("AppCode不正确，请到用户后台获取正确的AppCode： https://market.console.aliyun.com/imageconsole/index.htm")
        elif (status == 400 and msg == 'Invalid Path or Method'):
            print("url地址或请求的'GET'|'POST'方式不对")
        elif (status == 403 and msg == 'Unauthorized'):
            print("服务未被授权,请检查是否购买")
        elif (status == 403 and msg == 'Quota Exhausted'):
            print("套餐资源包次数已用完")
        elif (status == 500):
            print("API网关错误")
        else:
            print("参数名错误或其他错误")
            print(status)
            print(msg)

    print("---------response body is:-------------")
    print(html.text)

def kuaidiwuliu(request):
    data = {}
    c = []
    cursor1 = connection.cursor()
    cursor1.execute("SELECT * FROM `j_kuaidi` where id >= 64554")
    #cursor1.execute("SELECT * FROM `j_kuaidi`")
    raw = cursor1.fetchall()  # 读取所有s
    for ar in raw:
        appcode = "1fb56623de844f1bb2de46c28a2db5cf"
        req_data = {
            'com': 'auto',
            'nu': ar[1],
            'receiverPhone': '',
            'senderPhone': ''
        }
        url = "http://ali-deliver.showapi.com/showapi_expInfo"
        headers = {
            'Authorization': 'APPCODE ' + appcode
        }
        print(req_data)
        print(headers)
        try:
            html = requests.get(url, headers=headers, data=req_data)

        except:
            print("URL错误")
            exit()
        msg = html.headers.get('X-Ca-Error-Message')
        status = html.status_code
        if status == 200:
            dict_str = json.loads(html.text)
            code = ar[1]
            msg = "成功"
            kuaidigongsi = dict_str['showapi_res_body']['expTextName']
            if dict_str['showapi_res_body']['flag'] == True:
                print(dict_str['showapi_res_body'])
                shifadi = dict_str['showapi_res_body']['data'][0]['context'][0:5]
                shifa_shijian = dict_str['showapi_res_body']['data'][0]['time']
                daodadi = dict_str['showapi_res_body']['data'][-1]['context'][0:5]
                daoda_shijian = dict_str['showapi_res_body']['data'][-1]['time']
                cursor2 = connection.cursor()
                cursor2.execute("INSERT INTO j_kuaidifenjie (code,msg,shifadi,shifa_shijian,daodadi,daoda_shijian,kuaidigongsi) VALUES ('" + code + "','" + msg + "','" + shifadi + "','" + shifa_shijian + "','" + daodadi + "','" + daoda_shijian + "','" + kuaidigongsi + "')")
                raw2 = cursor2.fetchall()  # 读取所有
            else:

                cursor2 = connection.cursor()
                cursor2.execute(
                    "INSERT INTO j_kuaidifenjie (code,msg,kuaidigongsi) VALUES ('" + code + "','" + msg + "','" + kuaidigongsi + "')")
                raw2 = cursor2.fetchall()  # 读取所有
            print(dict_str['showapi_res_body']['flag'])
        else:
            if (status == 400 and msg == 'Invalid AppCode'):
                print("AppCode不正确，请到用户后台获取正确的AppCode： https://market.console.aliyun.com/imageconsole/index.htm")
            elif (status == 400 and msg == 'Invalid Path or Method'):
                print("url地址或请求的'GET'|'POST'方式不对")
            elif (status == 403 and msg == 'Unauthorized'):
                print("服务未被授权,请检查是否购买")
            elif (status == 403 and msg == 'Quota Exhausted'):
                print("套餐资源包次数已用完")
            elif (status == 500):
                print("API网关错误")
            else:
                cursor2 = connection.cursor()
                code = ar[1]
                dict_str = json.loads(html.text)
                kuaidigongsi = dict_str['showapi_res_body']['expTextName']
                cursor2.execute(
                    "INSERT INTO j_kuaidifenjie (code,msg,kuaidigongsi) VALUES ('" + code + "','错误','" + kuaidigongsi + "')")
                raw2 = cursor2.fetchall()  # 读取所有

    return HttpResponse()


if __name__ == "__main__":
    kuaidiwuliu()
