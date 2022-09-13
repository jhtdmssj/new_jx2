# # -*- coding: utf-8 -*-
import os

from django.db import connection
from django.http import JsonResponse, HttpResponse


def performance2020(request):
    data = {}
    c = []
    c3 = []
    c4 = []
    pci = []  # p次
    xingming = []  # 姓名
    cursor1 = connection.cursor()
    cursor2 = connection.cursor()
    cursor3 = connection.cursor()
    wanchengzongliang = []
    wczl_count = []

    renwumubiao = []
    caijipinliang = []
    feicaijipinliang = []

    # 第一层拿p次
    cursor3.execute("SELECT DISTINCT(shujuzhouqi) FROM jx_new_jixiao where nian='2020' order by id asc")
    raw3 = cursor3.fetchall()  # 读取所有
    for ar3 in raw3:
        pci.append(ar3[0])

    # 第二层拿人名
    cursor3.execute("SELECT DISTINCT(xingming) FROM `jx_new_jixiao` where nian='2020' order by quyu ASC,xingming ASC")
    raw3 = cursor3.fetchall()  # 读取所有
    for ar3 in raw3:
        xingming.append(ar3[0])
        # 第三层拿个人统计
    for i in pci:
        # i=2021P1 2021P2
        wczl = []
        wanchengzongliang = []
        mubiao_wis = []
        wis_caijipin = []
        wis_feicaiji = []
        # j=陈倩
        cursor3.execute(
            "SELECT shujuzhouqi,chengshi,xingming,sum(jixiaowancheng_wis),sum(mubiao_wis),sum(wis_caijipin),sum(wis_feicaiji) FROM `jx_new_jixiao` where shujuzhouqi='" + i + "'  group by shujuzhouqi,xingming ORDER BY quyu ASC,xingming ASC")
        raw3 = cursor3.fetchall()  # 读取所有
        # 相加完成 姓名：总数
        for ar3 in raw3:
            wanchengzongliang.append(ar3[3])
            mubiao_wis.append(ar3[4])
            wis_caijipin.append(ar3[5])
            wis_feicaiji.append(ar3[6])
        wczl.append({
            'wanchengzongliang': wanchengzongliang,
            'mubiao_wis': mubiao_wis,
            'wis_caijipin': wis_caijipin,
            'wis_feicaiji': wis_feicaiji,
        })

        c4.append({ar3[0]: wczl})

    c4.append({
        'pci': pci,
        'xingming': xingming,
    })

    # 总数
    z_wczl = []
    z_wanchengzongliang = []
    z_mubiao_wis = []
    z_wis_caijipin = []
    z_wis_feicaiji = []
    cursor2.execute(
        "SELECT shujuzhouqi,chengshi,xingming,sum(jixiaowancheng_wis),sum(mubiao_wis),sum(wis_caijipin),sum(wis_feicaiji) FROM `jx_new_jixiao`  where nian='2020'  group by xingming ORDER BY id asc")
    raw2 = cursor2.fetchall()  # 读取所有
    for ar2 in raw2:
        z_wanchengzongliang.append(ar2[3])
        z_mubiao_wis.append(ar2[4])
        z_wis_caijipin.append(ar2[5])
        z_wis_feicaiji.append(ar2[6])
    z_wczl.append({
        'z_wanchengzongliang': z_wanchengzongliang,
        'z_mubiao_wis': z_mubiao_wis,
        'z_wis_caijipin': z_wis_caijipin,
        'z_wis_feicaiji': z_wis_feicaiji,
    })

    c4.append({'all': z_wczl})

    data['list'] = (list(c4))
    print(data)
    return JsonResponse(data)


# 绩效
def performance(request):
    data = {}
    c = []
    c3 = []
    c4 = []
    pci = []  # p次
    xingming = []  # 姓名
    cursor1 = connection.cursor()
    cursor2 = connection.cursor()
    cursor3 = connection.cursor()
    wanchengzongliang = []
    wczl_count = []

    renwumubiao = []
    caijipinliang = []
    feicaijipinliang = []

    # 第一层拿p次
    cursor3.execute("SELECT DISTINCT(shujuzhouqi) FROM jx_new_jixiao where nian='2021' order by id asc")
    raw3 = cursor3.fetchall()  # 读取所有
    for ar3 in raw3:
        pci.append(ar3[0])

    # 第二层拿人名
    cursor3.execute("SELECT DISTINCT(xingming) FROM `jx_new_jixiao` where nian='2021' group by xingming order by quyu ASC,xingming ASC")
    raw3 = cursor3.fetchall()  # 读取所有
    for ar3 in raw3:
        xingming.append(ar3[0])

    # 第三层拿个人统计
    for i in pci:

            # i=2021P1 2021P2
            wczl = []
            wanchengzongliang = []
            mubiao_wis = []
            wis_caijipin = []
            wis_feicaiji = []
            # j=陈倩
            cursor3.execute(
                "SELECT shujuzhouqi,chengshi,xingming,sum(jixiaowancheng_wis),sum(mubiao_wis),sum(wis_caijipin),sum(wis_feicaiji) FROM `jx_new_jixiao` where shujuzhouqi='" + i + "' group by xingming ORDER BY quyu ASC,xingming ASC")
            raw3 = cursor3.fetchall()  # 读取所有
            # 相加完成 姓名：总数
            for ar3 in (raw3):
                wanchengzongliang.append(ar3[3])
                mubiao_wis.append(ar3[4])
                wis_caijipin.append(ar3[5])
                wis_feicaiji.append(ar3[6])
                wczl.append({
                    'wanchengzongliang': wanchengzongliang,
                    'mubiao_wis': mubiao_wis,
                    'wis_caijipin': wis_caijipin,
                    'wis_feicaiji': wis_feicaiji,
                })

                c4.append({ar3[0]: wczl})

    c4.append({
        'pci': pci,
        'xingming': xingming,
    })

    # 总数
    z_wczl = []
    z_wanchengzongliang = []
    z_mubiao_wis = []
    z_wis_caijipin = []
    z_wis_feicaiji = []
    cursor2.execute(
        "SELECT shujuzhouqi,chengshi,xingming,sum(jixiaowancheng_wis),sum(mubiao_wis),sum(wis_caijipin),sum(wis_feicaiji) FROM `jx_new_jixiao`  where nian='2021' group by xingming ORDER BY id asc")
    raw2 = cursor2.fetchall()  # 读取所有
    for ar2 in raw2:
        z_wanchengzongliang.append(ar2[3])
        z_mubiao_wis.append(ar2[4])
        z_wis_caijipin.append(ar2[5])
        z_wis_feicaiji.append(ar2[6])
    z_wczl.append({
        'z_wanchengzongliang': z_wanchengzongliang,
        'z_mubiao_wis': z_mubiao_wis,
        'z_wis_caijipin': z_wis_caijipin,
        'z_wis_feicaiji': z_wis_feicaiji,
    })

    c4.append({'all': z_wczl})

    data['list'] = (list(c4))
    return JsonResponse(data)
