import logging
import os

import requests
import json
import time
from django.http import JsonResponse, HttpResponse
from houtai.pymysql_tool import pymysql_tool


def daochu(request):
    LOG_FORMAT = "%(asctime)s %(name)s %(levelname)s %(pathname)s %(message)s "  # 配置输出日志格式
    DATE_FORMAT = '%Y-%m-%d  %H:%M:%S %a '  # 配置输出时间的格式，注意月份和天数不要搞乱了
    logging.basicConfig(level=logging.DEBUG,
                        format=LOG_FORMAT,
                        datefmt=DATE_FORMAT,
                        filename=r"/new_jx/houtai/log.log"
                        # 有了filename参数就不会直接输出显示到控制台，而是直接写入文件
                        )


    db = pymysql_tool()
    # 获取token
    url = "https://dataapi.bazhuayu.com/token"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'username': 'CTR1696',
        'password': '19810525a',
        'grant_type': 'password'
    }
    rs = requests.post(url=url, headers=headers, data=data)
    e2 = json.loads(rs.text)
    access_token = e2['access_token']
    refresh_token = e2['refresh_token']

    size = 1000
    # 第一次
    header = {
        'Content-Type': 'application/json',
        'Authorization': 'bearer' + ' ' + access_token
    }
    url2 = "https://dataapi.bazhuayu.com/api/alldata/GetDataOfTaskByOffset"
    data2 = {
        "taskId": "db871981-f22e-3187-fdb0-6b8b9303bf0b",
        "size": size,
        "offset": 0
    }
    rs2 = requests.get(url=url2, params=data2, headers=header)
    rs2 = json.loads(rs2.text)
    offset = rs2['data']['offset']
    # 第一次
    for i in range(size):  # 1000W
        dianshang = rs2['data']['dataList'][i]['电商渠道']
        yiji = rs2['data']['dataList'][i]['一级类目']
        erji = rs2['data']['dataList'][i]['二级类目']
        shangpinliang = rs2['data']['dataList'][i]['商品量']
        dianpuid = rs2['data']['dataList'][i]['店铺ID']
        dianpumingcheng = rs2['data']['dataList'][i]['店铺名称']
        shangpinid = rs2['data']['dataList'][i]['商品ID']
        pinpai = rs2['data']['dataList'][i]['品牌']
        shangpintiaoma = rs2['data']['dataList'][i]['商品条码']
        quancheng = rs2['data']['dataList'][i]['全称']
        jiage = rs2['data']['dataList'][i]['价格']
        wangzhi = rs2['data']['dataList'][i]['网址']
        pinglunliang = rs2['data']['dataList'][i]['评论量']
        zhuaqushijian = rs2['data']['dataList'][i]['抓取时间']
        pinleidaima = rs2['data']['dataList'][i]['品类代码']
        pinlei = rs2['data']['dataList'][i]['品类']

        try:
            sql = "INSERT INTO bazhuayu (dianshang,yiji,erji,shangpinliang,dianpuid,dianpumingcheng,shangpinid,pinpai,shangpintiaoma,quancheng,jiage,wangzhi,pinglunliang,zhuaqushijian,pinleidaima,pinlei) VALUES ('" + str(
                dianshang) + "','" + str(yiji) + "','" + str(erji) + "','" + str(shangpinliang) + "', '" + str(
                dianpuid) + "', '" + str(dianpumingcheng) + "', '" + str(shangpinid) + "', '" + str(
                pinpai) + "', '" + str(shangpintiaoma) + "', '" + str(quancheng) + "', '" + str(
                jiage) + "', '" + str(wangzhi) + "', '" + str(pinglunliang) + "','" + str(
                zhuaqushijian) + "', '" + str(pinleidaima) + "', '" + str(pinlei) + "')"
            db.change(sql)

        except Exception as e:
            print('except:', e)
            break
    ofst = offset
    while True:
        if (ofst<0):
            break
        else:
            # 无限循环
            header = {
                'Content-Type': 'application/json',
                'Authorization': 'bearer' + ' ' + access_token
            }
            url2 = "https://dataapi.bazhuayu.com/api/alldata/GetDataOfTaskByOffset"
            print(ofst)
            data2 = {
                "taskId": "db871981-f22e-3187-fdb0-6b8b9303bf0b",
                "size": size,
                "offset": ofst
            }
            rs2 = requests.get(url=url2, params=data2, headers=header)
            rs3 = json.loads(rs2.text)
            ofst = rs3['data']['offset']
            try:
                for i in range(size):  # 1000W
                    dianshang = rs3['data']['dataList'][i]['电商渠道']
                    yiji = rs3['data']['dataList'][i]['一级类目']
                    erji = rs3['data']['dataList'][i]['二级类目']
                    shangpinliang = rs3['data']['dataList'][i]['商品量']
                    dianpuid = rs3['data']['dataList'][i]['店铺ID']
                    dianpumingcheng = rs3['data']['dataList'][i]['店铺名称']
                    shangpinid = rs3['data']['dataList'][i]['商品ID']
                    pinpai = rs3['data']['dataList'][i]['品牌']
                    shangpintiaoma = rs3['data']['dataList'][i]['商品条码']
                    quancheng = rs3['data']['dataList'][i]['全称']
                    jiage = rs3['data']['dataList'][i]['价格']
                    wangzhi = rs3['data']['dataList'][i]['网址']
                    pinglunliang = rs3['data']['dataList'][i]['评论量']
                    zhuaqushijian = rs3['data']['dataList'][i]['抓取时间']
                    pinleidaima = rs3['data']['dataList'][i]['品类代码']
                    pinlei = rs3['data']['dataList'][i]['品类']

                    try:
                        sql = "INSERT INTO bazhuayu (dianshang,yiji,erji,shangpinliang,dianpuid,dianpumingcheng,shangpinid,pinpai,shangpintiaoma,quancheng,jiage,wangzhi,pinglunliang,zhuaqushijian,pinleidaima,pinlei) VALUES ('" + str(
                            dianshang) + "','" + str(yiji) + "','" + str(erji) + "','" + str(shangpinliang) + "', '" + str(
                            dianpuid) + "', '" + str(dianpumingcheng) + "', '" + str(shangpinid) + "', '" + str(
                            pinpai) + "', '" + str(shangpintiaoma) + "', '" + str(quancheng) + "', '" + str(
                            jiage) + "', '" + str(wangzhi) + "', '" + str(pinglunliang) + "','" + str(
                            zhuaqushijian) + "', '" + str(pinleidaima) + "', '" + str(pinlei) + "')"
                        db.change(sql)
                        time.sleep(0.1)
                    except Exception as e:
                        logging.error('except:', e)
                        break
                logging.info(ofst)
            except Exception as e:
                   logging.error('except:', e)
    return HttpResponse()
