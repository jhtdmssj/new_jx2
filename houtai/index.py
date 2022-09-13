# # -*- coding: utf-8 -*-
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


def timec(request):
    # 获取今天是第几周
    return HttpResponse()


def login(request):
    username = request.GET.get('value1')
    password2 = request.GET.get('value2')
    list = User.objects.filter(name=username).filter(password=password2)
    if list:
        for var in list:
            response1 = var.name
            response2 = var.password
            # request.session['dj_name'] = var.name

            return JsonResponse({'code': 2, 'message': '登录成功_您好：' + response1 + '', 'user': response1})
    else:
        return JsonResponse({'code': 1, 'message': '用户名或密码错误，请重新输入'})
    return


# 后台跑库 已经忘记干嘛用的了（- -！）
def houtai_jx(request):
    # 第一步 jx_jixiao表里的内容全部删除
    jx_jixiao.objects.all().delete()

    data = {}
    c = []
    renwul = ''
    sz = ''
    # 判断是否有查询
    if request.GET.get('pici'):
        pici = request.GET.get('pici')
        week = request.GET.get('week')
    else:
        # pici 当前月的批次 week当前月的周
        pici = '1'
        week = '2'
    # 创建链接
    cursor1 = connection.cursor()
    caiji = connection.cursor()
    caiji2 = connection.cursor()
    caiji3 = connection.cursor()
    feicaiji = connection.cursor()
    xp_zl = connection.cursor()
    xp_kh = connection.cursor()
    xp_zd = connection.cursor()
    xp_ql = connection.cursor()
    fkl_wis = connection.cursor()
    fkl_wis_2 = connection.cursor()
    fkl_cg = connection.cursor()
    fkl_cg_2 = connection.cursor()
    fkl_ql = connection.cursor()
    xiujia = connection.cursor()
    fkl_ql_zl = connection.cursor()
    mydata = connection.cursor()

    # 基础表
    cursor1.execute(
        "SELECT * FROM `jx_zhouqibiao`,`user`,`jx_zhourenwu` WHERE USER.qx = '4' AND jx_zhourenwu.user_id=user.id and pici='9' and zhou='2'")
    raw = cursor1.fetchall()  # 读取所有
    # 获取当前系统日期
    dqdate = datetime.datetime.now().strftime('%Y-%m-%d')

    for ar in raw:
        # 如果当前日期小于等于 绩效日期 就停止
        # if dqdate <= ar[9] :
        #    break
        # else :

        # 周期2020P1-1
        zhouqi = str(ar[1]) + str(ar[2]) + str(ar[3]) + "-" + str(ar[4])
        # ar[4] 批次是周
        if ar[4] == '1':
            renwul = round(int(ar[29]) * 0.2)
        elif ar[4] == '2':
            renwul = round(int(ar[29]) * 0.28)
        elif ar[4] == '3':
            renwul = round(int(ar[29]) * 0.32)
        elif ar[4] == '4':
            renwul = round(int(ar[29]) * 0.2)
        elif ar[4] == '5':
            renwul = round(int(ar[29]) * 0.24)

        # ar[9]是kaishiri
        # ar[10]是jiesuri
        # ar[18]是人名
        # ar[23]是地区

        # wis采集
        # #总值
        # caiji.execute("SELECT COUNT( DISTINCT id) FROM  w_commodity WHERE submittime >= '"+ar[9]+"' AND submittime <= '"+ar[10]+"' AND datatype != 1 AND categoryid != '9001' and categoryid < '899' AND realname = '"+ar[18]+"' and cityname = '"+ar[23]+"' AND status != 4;")
        # raw2 = caiji.fetchone()
        # 普通
        caiji.execute(
            "SELECT COUNT( DISTINCT id) FROM  w_commodity WHERE submittime >= '" + ar[9] + "' AND submittime <= '" + ar[
                10] + "' AND datatype != 1 AND categoryid != '9001' and categoryid < '899' AND realname = '" + ar[
                18] + "' and cityname = '" + ar[23] + "' AND status != 4 and brandtype!=2 and categoryid!='9999'")
        raw2_brandtype2 = caiji.fetchone()
        # 不是客户 等于组合装
        caiji2.execute(
            "SELECT COUNT( DISTINCT id) FROM  w_commodity WHERE submittime >= '" + ar[9] + "' AND submittime <= '" + ar[
                10] + "' AND datatype != 1 AND categoryid != '9001' AND realname = '" + ar[18] + "' and cityname = '" +
            ar[23] + "' AND status != 4 and categoryid='9999' and  brandtype!=2")
        raw2_zuhe = caiji2.fetchone()
        # 客户
        caiji3.execute(
            "SELECT COUNT( DISTINCT id) FROM  w_commodity WHERE submittime >= '" + ar[9] + "' AND submittime <= '" + ar[
                10] + "' AND datatype != 1 AND categoryid != '9001' AND realname = '" + ar[18] + "' and cityname = '" +
            ar[23] + "' AND status != 4  and brandtype=2")
        raw2_kehu = caiji3.fetchone()

        raw2 = round(int(raw2_brandtype2[0]) + int(raw2_zuhe[0]) * 1.3 + int(raw2_kehu[0]) * 1.3)

        # wis非采集  N %1 = 1开头 N %2 = 2开头
        feicaiji.execute(
            "SELECT COUNT( DISTINCT id ) FROM w_commodity WHERE datatype > 1 	AND categoryid >= '899' AND categoryid <> '9001'  AND categoryid <> '9999'  AND barcode not like (N'978%') and commodityname not like (N'%非%码%') AND barcode not like (N'1%') AND barcode not like (N'2%') AND status != 4 AND submittime >= '" +
            ar[9] + "' AND submittime <= '" + ar[10] + "' AND realname = '" + ar[18] + "' and cityname='" + ar[
                23] + "'")
        raw3 = feicaiji.fetchone()

        # 新品采集总量
        xp_zl.execute(
            "SELECT COUNT( DISTINCT id ) FROM w_commodity WHERE datatype = 1 AND categoryid != '9001' AND submittime >= '" +
            ar[9] + "' AND submittime <= '" + ar[10] + "' AND realname = '" + ar[
                18] + "' AND status != 4 and cityname='" + ar[23] + "'")
        raw6 = xp_zl.fetchone()

        # 新品采集客户
        xp_kh.execute(
            "SELECT COUNT( DISTINCT id ) FROM w_commodity WHERE datatype = 1 AND categoryid != '9001' AND submittime >= '" +
            ar[9] + "' AND submittime <= '" + ar[10] + "' AND realname = '" + ar[
                18] + "' AND brandtype = '2' AND status != 4 and cityname='" + ar[23] + "'")
        raw4 = xp_kh.fetchone()

        # 新品采集重点
        xp_zd.execute(
            "SELECT COUNT( DISTINCT id ) FROM w_commodity WHERE datatype = 1 AND categoryid != '9001' AND submittime >= '" +
            ar[9] + "' AND submittime <= '" + ar[10] + "' AND realname = '" + ar[
                18] + "' AND brandtype = '1'AND status != 4 and cityname='" + ar[23] + "'")
        raw5 = xp_zd.fetchone()

        # 新品采集麒麟
        xp_ql.execute("SELECT COUNT( DISTINCT id ) FROM w_commodity WHERE categoryid = '9001' AND submittime >= '" + ar[
            9] + "' AND submittime <= '" + ar[10] + "' AND status != 4 and realname = '" + ar[18] + "' and cityname='" +
                      ar[23] + "'")
        raw7 = xp_ql.fetchone()

        # 通过率 wis总数
        fkl_wis_2.execute(
            "SELECT COUNT( DISTINCT id ) FROM w_commodity WHERE categoryid != '9001' AND submittime >= '" + ar[
                9] + "' AND submittime <= '" + ar[10] + "' and datatype!='1' AND realname = '" + ar[
                18] + "' and cityname='" + ar[23] + "'")
        raw8_2 = fkl_wis_2.fetchone()

        # 通过率_wis
        fkl_wis.execute(
            "SELECT COUNT( DISTINCT id ) FROM w_commodity WHERE categoryid != '9001' AND submittime >= '" + ar[
                9] + "' AND submittime <= '" + ar[10] + "' and datatype!='1' AND STATUS != 4 AND realname = '" + ar[
                18] + "' and cityname='" + ar[23] + "'")
        raw8 = fkl_wis.fetchone()
        if raw8[0] == 0 or raw8_2[0] == 0:
            tgl_wis = 0
        else:
            tgl_wis = round(raw8[0] / raw8_2[0] * 100, 2)

        # 通过率_常规
        fkl_cg.execute(
            "SELECT COUNT( DISTINCT id) FROM	w_commodity WHERE submittime >= '" + ar[9] + "' AND submittime <= '" +
            ar[10] + "' AND status != 4 AND datatype = '1' AND categoryid != '9001' and realname='" + ar[
                18] + "' and cityname='" + ar[23] + "'")
        raw9 = fkl_cg.fetchone()  # 读取所有

        fkl_cg_2.execute(
            "SELECT COUNT( DISTINCT id) FROM w_commodity WHERE submittime >= '" + ar[9] + "' AND submittime <= '" + ar[
                10] + "' AND datatype = '1' AND categoryid != '9001' and realname='" + ar[18] + "' and cityname='" + ar[
                23] + "'")
        raw9_zl = fkl_cg_2.fetchone()  # 读取所有
        if raw9[0] == 0 or raw9_zl[0] == 0:
            tgl_cg = 0
        else:
            tgl_cg = round(raw9[0] / raw9_zl[0] * 100, 2)

        # 通过率_麒麟
        fkl_ql.execute(
            "SELECT COUNT( DISTINCT id) FROM w_commodity WHERE submittime >= '" + ar[9] + "' AND submittime <= '" + ar[
                10] + "' AND status != 4 AND categoryid = '9001' and realname='" + ar[18] + "' and cityname='" + ar[
                23] + "'")
        raw10 = fkl_ql.fetchone()  # 读取所有
        fkl_ql_zl.execute(
            "SELECT COUNT( DISTINCT id) FROM w_commodity WHERE submittime >= '" + ar[9] + "' AND submittime <= '" + ar[
                10] + "' AND categoryid = '9001' and realname='" + ar[18] + "' and cityname='" + ar[23] + "'")
        raw10_zl = fkl_ql_zl.fetchone()  # 读取所有
        if raw10[0] == 0 or raw10_zl[0] == 0:
            tgl_ql = 0
        else:
            tgl_ql = round(raw10[0] / raw10_zl[0] * 100, 2)

        # 3周绩效
        # 自动评价 基础任务目标 wis—任务 renwul 绩效统计wis-任务 round(raw2[0]+raw2[0]*0.8)
        # 正常周：ar[13]  sz="是否申请三周绩效"
        pci = ar[2] + ar[3]
        xiujia.execute("SELECT * FROM sanzhoujixiao WHERE name='" + ar[18] + "' and pci='" + pci + "'")
        raw111 = xiujia.fetchall()  # 读取所有
        if raw111 == None:
            sz = "否"
        else:
            for arr in raw111:
                if arr[2] == pci and arr[3] == ar[4]:
                    sz = "是"
                else:
                    sz = "否"
        jc_wis = renwul
        jx_wis = round(raw2 + raw3[0] * 0.8)
        # jc_wis jx_wis wis总数
        if jc_wis == 0 or jx_wis == 0:
            jz = "不达标"
            jl = 0
        else:
            if ar[13] == "正常周":
                if sz == "否":
                    if round(jx_wis / jc_wis, 2) >= 1.75:
                        jz = "荣耀奖"
                        if ar[4] == '1':
                            jl = 110
                        elif ar[4] == '2':
                            jl = 154
                        elif ar[4] == '3':
                            jl = 176
                        elif ar[4] == '4':
                            jl = 110
                        elif ar[4] == '5':
                            jl = 110
                    elif round(jx_wis / jc_wis, 2) >= 1.45 and round(jc_wis / jx_wis, 2) < 1.75:
                        jz = "星光奖"
                        if ar[4] == '1':
                            jl = 80
                        elif ar[4] == '2':
                            jl = 112
                        elif ar[4] == '3':
                            jl = 128
                        elif ar[4] == '4':
                            jl = 80
                        elif ar[4] == '5':
                            jl = 80
                    elif round(jx_wis / jc_wis, 2) >= 1 and round(jc_wis / jx_wis, 2) < 1.45:
                        jz = "达标"
                        jl = 0
                    else:
                        jz = "不达标"
                        jl = 0
                else:
                    if round(jx_wis / jc_wis, 2) >= 1.5:
                        jz = "星光奖"
                        jl = 0
                    elif round(jx_wis / jc_wis, 2) >= 0.75 and round(jc_wis / jx_wis, 2) < 1.5:
                        jz = "达标"
                        jl = 0
                    elif round(jx_wis / jc_wis, 2) < 0.75:
                        jz = "不达标"
                        jl = 0
            else:
                if jx_wis > jc_wis:
                    jz = "达标"
                    jl = 0
                else:
                    jz = "不达标"
                    jl = 0

        # 麒麟和常规任务不达标降档
        if ar[4] == '1':
            if (raw7[0] < 5 and raw6[0] >= 5) or (raw7[0] >= 5 and raw6[0] < 5):
                if jz == "荣耀奖":
                    jz = "星光奖"
                    jl = 80
                elif jz == "星光奖":
                    jz = "达标"
                    jl = 0
                elif jz == "达标":
                    jz = "不达标"
                    jl = 0
            elif raw7[0] < 5 and raw6[0] < 5:
                if jz == "荣耀奖":
                    jz = "达标"
                    jl = 0
                elif jz == "星光奖":
                    jz = "不达标"
                    jl = 0
                elif jz == "达标":
                    jz = "不达标"
                    jl = 0

        elif ar[4] == '2':
            if (raw7[0] < 5 and raw6[0] >= 5) or (raw7[0] >= 5 and raw6[0] < 5):
                if jz == "荣耀奖":
                    jz = "星光奖"
                    jl = 112
                elif jz == "星光奖":
                    jz = "达标"
                    jl = 0
                elif jz == "达标":
                    jz = "不达标"
                    jl = 0
            elif raw7[0] < 5 and raw6[0] < 5:
                if jz == "荣耀奖":
                    jz = "达标"
                    jl = 0
                elif jz == "星光奖":
                    jz = "不达标"
                    jl = 0
                elif jz == "达标":
                    jz = "不达标"
                    jl = 0

        elif ar[4] == '3':
            if (raw7[0] < 5 and raw6[0] >= 5) or (raw7[0] >= 5 and raw6[0] < 5):
                if jz == "荣耀奖":
                    jz = "星光奖"
                    jl = 128
                elif jz == "星光奖":
                    jz = "达标"
                    jl = 0
                elif jz == "达标":
                    jz = "不达标"
                    jl = 0
            elif raw7[0] < 5 and raw6[0] < 5:
                if jz == "荣耀奖":
                    jz = "达标"
                    jl = 0
                elif jz == "星光奖":
                    jz = "不达标"
                    jl = 0
                elif jz == "达标":
                    jz = "不达标"
                    jl = 0

        elif ar[4] == '4':
            if (raw7[0] < 5 and raw6[0] >= 5) or (raw7[0] >= 5 and raw6[0] < 5):
                if jz == "荣耀奖":
                    jz = "星光奖"
                    jl = 80
                elif jz == "星光奖":
                    jz = "达标"
                    jl = 0
                elif jz == "达标":
                    jz = "不达标"
                    jl = 0
            elif raw7[0] < 5 and raw6[0] < 5:
                if jz == "荣耀奖":
                    jz = "达标"
                    jl = 0
                elif jz == "星光奖":
                    jz = "不达标"
                    jl = 0
                elif jz == "达标":
                    jz = "不达标"
                    jl = 0

        elif ar[4] == '5':
            if (raw7[0] < 5 and raw6[0] >= 5) or (raw7[0] >= 5 and raw6[0] < 5):
                if jz == "荣耀奖":
                    jz = "星光奖"
                    jl = 0
                elif jz == "星光奖":
                    jz = "达标"
                    jl = 0
                elif jz == "达标":
                    jz = "不达标"
                    jl = 0
            elif raw7[0] < 5 and raw6[0] < 5:
                if jz == "荣耀奖":
                    jz = "达标"
                    jl = 0
                elif jz == "星光奖":
                    jz = "不达标"
                    jl = 0
                elif jz == "达标":
                    jz = "不达标"
                    jl = 0

        # 占比1
        if raw4[0] == 0 or raw6[0] == 0:
            zb1 = 0
        else:
            zb1 = str(round(raw4[0] / raw6[0] * 100)) + '%'
        # 占比1
        if raw5[0] == 0 or raw6[0] == 0:
            zb2 = 0
        else:
            zb2 = str(round(raw5[0] / raw6[0] * 100)) + '%'

        # mydata 任务量
        # 获取当前周的 日期 monday是 本周的 星期一 sunday是本周的星期天
        # monday, sunday = datetime.date.today(), datetime.date.today()
        # one_day = datetime.timedelta(days=1)
        # while monday.weekday() != 0:
        #     monday -= one_day
        # while sunday.weekday() != 6:
        #     sunday += one_day
        mydata.execute("SELECT count(*) FROM mission_up where querentime between '" + ar[9] + "' and '" + ar[
            10] + "' and querenren='" + ar[18] + "'")
        raw_mydata = mydata.fetchone()  # 读取所有

        # ar[8]代表没周结束日
        # dqtime 本地时间的 年月 日的日
        # dqtime_nian=ar[8].split('-')
        # if str(dqtime_nian[2]) > '21' :
        #     dqtime_zhouqi = str((dqtime_nian[0]) + (dqtime_nian[1]))
        #     dqtime_zhouqi = int(zhouqi) + 1
        # else:
        #     dqtime_zhouqi = (str(dqtime_nian[0]) + str(dqtime_nian[1]))

        c.append({
            'nianfen': zhouqi,
            'pj': ar[2],
            'pici': ar[3],
            'zhou': ar[4],
            'shujuzhouqi': ar[5],
            'kaohezhouqi': ar[6],
            'sj_kaishiri': ar[7],
            'sj_jiesuri': ar[8],
            'ke_kaishiri': ar[9],
            'ke_jiesuri': ar[10],
            'week': ar[11],
            'jidu': ar[12],
            'jiexiaoleixing': ar[13],
            'beizhu': ar[14],
            'gongzizhouqi': ar[15],
            'name': ar[18],
            'quyu': ar[23],
            'diqu': ar[22],
            'renwuliang': renwul,
            'jcrw_changguirenwu': '5',
            'jcrw_qilin': '5',
            'wiscj_caijipin': raw2,
            'wiscj_feicaiji': raw3[0],
            'wiscj_zongliang': raw2 + raw3[0],
            'xpcj_zongliang': raw6[0],
            'xpcj_kehu': raw4[0],
            'xpcj_zhongdian': raw5[0],
            'xpcj_zhanbi': zb1,
            'xpcj_zhanbi2': zb2,
            'qlcjl_hegeshuliang': raw7[0],
            'fkl_wis': str(tgl_wis) + '%',
            'fkl_changgui': str(tgl_cg) + '%',
            'fkl_qilin': str(tgl_ql) + '%',
            'jxtj_wisrenwu': round(raw2 + raw3[0] * 0.8),
            'jxtj_changguirenwu': raw6[0],
            'jxtj_qilin': raw7[0],
            'sfxj_shifouxiujia': sz,
            'zdpj_pingjia': jz,
            'mydata_mydataqueren': raw_mydata[0],
            'zdpj_jiangli': jl,
            # 'lwjs_zhouqi': dqtime_zhouqi,
            # 'sjqr_tiaozheng':raw[42]
        })
        tst = jx_jixiao(
            nianfen=zhouqi,
            pj=ar[2],
            pici=ar[3],
            zhou=ar[4],
            shujuzhouqi=ar[5],
            kaohezhouqi=ar[6],
            sj_kaishiri=ar[7],
            sj_jiesuri=ar[8],
            ke_kaishiri=ar[9][:-8],
            ke_jiesuri=ar[10][:-8],
            week=ar[11],
            jidu=ar[12],
            jiexiaoleixing=ar[13],
            beizhu=ar[14],
            gongzizhouqi=ar[15],
            name=ar[18],
            quyu=ar[23],
            diqu=ar[22],
            renwuliang=renwul,
            jcrw_changguirenwu='5',
            jcrw_qilin='5',
            wiscj_caijipin=raw2,
            wiscj_feicaiji=raw3[0],
            wiscj_zongliang=raw2 + raw3[0],
            xpcj_zongliang=raw6[0],
            xpcj_kehu=raw4[0],
            xpcj_zhongdian=raw5[0],
            xpcj_zhanbi=zb1,
            xpcj_zhanbi2=zb2,
            qlcjl_hegeshuliang=raw7[0],
            fkl_wis=str(tgl_wis) + '%',
            fkl_changgui=str(tgl_cg) + '%',
            fkl_qilin=str(tgl_ql) + '%',
            jxtj_wisrenwu=round(raw2 + raw3[0] * 0.8),
            jxtj_changguirenwu=raw6[0],
            jxtj_qilin=raw7[0],
            sfxj_shifouxiujia=sz,
            zdpj_pingjia=jz,
            mydata=raw_mydata[0],
            zdpj_jiangli=jl,
            # lwjs_zhouqi=dqtime_zhouqi,
            # sjqr_tiaozheng=raw[42]
        ).save()

    data['list'] = (list(c))
    return JsonResponse(data, safe=False)


# 绩效表
def jixiao(request):
    data = {}
    if request.GET.get('pici'):
        pici = request.GET.get('pici')
        week = request.GET.get('week')
        book = jx_jixiao.objects.filter(pici=pici, zhou=week).all().values()  # 获取值values放后面
    else:
        book = jx_jixiao.objects.all().values()  # 获取值values放后面
    data['list'] = (list(book))
    return JsonResponse(data)


# 每周数据采集情况 表1
def tongjitubiao(request):
    data = {}
    c = []
    cursor1 = connection.cursor()
    # 基础表
    cursor1.execute(
        "SELECT caijipinshuliang,feicaishuliang,zhongxinchuli,changguitijiaoshuliang,zhouqi FROM `w_work_info_tmp` order by zhouqi desc limit 0,53")
    raw = cursor1.fetchall()  # 读取所有
    for ar in raw:
        c.append({
            'caijipinshuliang': str(ar[0]),
            'feicaishuliang': str(ar[1]),
            'zhongxinchuli': str(ar[2]),
            'changguitijiaoshuliang': str(ar[3]),
            'zhouqi': str(ar[4]),
        })
    data['list'] = (list(c))
    return JsonResponse(data)


# 提交量-P表 表2
def tijiaoliangP(request):
    data = {}
    c = []
    cursor1 = connection.cursor()
    # 基础表
    cursor1.execute(
        "SELECT * FROM (SELECT pci,newcount,wis,intercept,collect,uncollect,qilin FROM `w_monitor` order by pci desc ) aa ORDER BY pci")
    raw = cursor1.fetchall()  # 读取所有
    for ar in raw:
        c.append({
            'pci': str(ar[0]),
            'new_count': str(ar[1]),
            'wis': str(ar[2]),
            'uncollect_intercept': str(ar[3]),
            'collect': str(ar[4]),
            'uncollect': str(ar[5]),
            'qilin': str(ar[6]),
        })
    data['list'] = (list(c))
    return JsonResponse(data)


def tijiaoliangP2(request):
    data = {}
    c = []
    cursor1 = connection.cursor()
    # 基础表
    cursor1.execute(
        "SELECT * FROM (SELECT pci,newcount,wis,intercept,collect,uncollect,qilin FROM `w_monitor` ORDER BY pci desc limit 0,14 ) aa ORDER BY pci asc")
    raw = cursor1.fetchall()  # 读取所有
    for ar in raw:
        c.append({
            'pci': str(ar[0]),
            'new_count': str(ar[1]),
            'wis': str(ar[2]),
            'uncollect_intercept': str(ar[3]),
            'collect': str(ar[4]),
            'uncollect': str(ar[5]),
            'qilin': str(ar[6]),
        })
    data['list'] = (list(c))
    return JsonResponse(data)


# 常规数据抄录情况连续监测 表4
def changgui4(request):
    data = {}
    c = []
    cursor1 = connection.cursor()
    cursor1.execute("SELECT pci,newcount,importdata,havescandata FROM `w_monitor` order by year asc")
    raw = cursor1.fetchall()  # 读取所有
    for ar in raw:
        c.append({
            'pci': str(ar[0]),
            'newcount': str(ar[1]),
            'importdata': str(ar[2]),
            'havescandata': str(ar[3]),
        })
    data['list'] = (list(c))
    return JsonResponse(data)


# 常规数据抄录情况连续监测 表7
def changgui(request):
    data = {}
    all = []
    c = []
    newcount = []
    f = connection.cursor()
    cursor1 = connection.cursor()
    cursor2 = connection.cursor()
    # 基础表
    i = 0;

    f.execute("SELECT count(*) FROM `w_monitor` order by year asc")
    rawcount = f.fetchall()
    cursor1.execute("SELECT DISTINCT(year) FROM `w_monitor` order by year asc")
    raw = cursor1.fetchall()  # 读取所有

    data['list'] = (list(newcount))
    return JsonResponse(data)


# 新图表 表8
def xintubiao(request):
    data = {}
    c = []
    newcount = []
    cursor2 = connection.cursor()
    cursor2.execute(
        "SELECT riqi,weipipeitiaomaliang,tijiaoliang,pinci,pipeilv  FROM `w_unmatch_commit` order by riqi asc")
    raw = cursor2.fetchall()  # 读取所有
    for ar in raw:
        c.append({
            'riqi': str(ar[0]),
            'weipipeitiaomaliang': str(ar[1]),
            'tijiaoliang': str(ar[2]),
            'pinci': str(ar[3]),
            'pipeilv': str(ar[4]),
        })
    data['list'] = (list(c))
    return JsonResponse(data)


# 地方图表
def difangtubiao(request):
    data = {}
    c = []
    zrenwuliang = 0
    cursor1 = connection.cursor()
    cursor1.execute(
        "SELECT shujuzhouqi,diqu,GROUP_CONCAT(DISTINCT(name)) as name,sum(renwuliang) as renwuliang,sum(wiscj_caijipin) as wiscj_caijipin,sum(wiscj_feicaiji) as wiscj_feicaiji,sum(jcrw_changguirenwu) as jcrw_changguirenwu,sum(xpcj_zongliang) as xpcj_zongliang,sum(jcrw_qilin) as jcrw_qilin,sum(qlcjl_hegeshuliang) as qlcjl_hegeshuliang  from  `jx_jixiao`  group by name order by diqu asc;")
    raw = cursor1.fetchall()  # 读取所有
    for ar in raw:
        c.append({
            'shujuzhouqi': str(ar[0]),
            'diqu': str(ar[1]),
            'name': str(ar[2]),
            # WIS任务量
            'renwuliang': int(ar[3]),
            # 采集品
            'wiscj_caijipin': int(ar[4]),
            # 非采集
            'wiscj_feicaiji': int(ar[5]),
            # 常规任务量
            'jcrw_changguirenwu': int(ar[6]),
            # 新品采集 总量
            'xpcj_zongliang': int(ar[7]),
            # 麒麟
            'jcrw_qilin': int(ar[8]),
            # 麒麟量
            'qlcjl_hegeshuliang': int(ar[9]),

        })
    data['list'] = (list(c))
    return JsonResponse(data)


# 测试图表 2个 下拉框方法
# def difangtubiao_select1(request):
#     data = {}
#     c=[]
#     if request.GET.get('zhouqi'):
#         quyu =request.GET.get('zhouqi')
#         cursor1 = connection.cursor()
#         cursor1.execute("SELECT shujuzhouqi,diqu,name,renwuliang,wiscj_caijipin,wiscj_feicaiji,jcrw_changguirenwu,xpcj_zongliang,jcrw_qilin,qlcjl_hegeshuliang FROM `jx_jixiao` where diqu='"+str(quyu)+"'")
#         raw = cursor1.fetchall()  # 读取所有
#         for ar in raw:
#             c.append({
#                 'shujuzhouqi': str(ar[0]),
#                 'diqu': str(ar[1]),
#                 'name': str(ar[2]),
#                 #WIS任务量
#                 'renwuliang': str(ar[3]),
#                 #采集品
#                 'wiscj_caijipin': str(ar[4]),
#                 #非采集
#                 'wiscj_feicaiji': str(ar[5]),
#                 #常规任务量
#                 'jcrw_changguirenwu':str(ar[6]),
#                 #新品采集 总量
#                 'xpcj_zongliang':str(ar[7]),
#                 #麒麟
#                 'jcrw_qilin':str(ar[8]),
#                 #麒麟量
#                 'qlcjl_hegeshuliang':str(ar[9]),
#             })
#     data['list'] = (list(c))
#     return JsonResponse(data)
def difangtubiao_select2(request):
    data = {}
    c = []
    if request.GET.get('zhouqi'):
        zhouqi = request.GET.get('zhouqi')
        cursor1 = connection.cursor()
        cursor1.execute(
            "SELECT shujuzhouqi,diqu,GROUP_CONCAT(DISTINCT(name)) as name,sum(renwuliang) as renwuliang,sum(wiscj_caijipin) as wiscj_caijipin,sum(wiscj_feicaiji) as wiscj_feicaiji,sum(jcrw_changguirenwu) as jcrw_changguirenwu,sum(xpcj_zongliang) as xpcj_zongliang,sum(jcrw_qilin) as jcrw_qilin,sum(qlcjl_hegeshuliang) as qlcjl_hegeshuliang  from  `jx_jixiao` where shujuzhouqi='" + str(
                zhouqi) + "' group by name order by diqu asc")
        raw = cursor1.fetchall()  # 读取所有
        for ar in raw:
            c.append({
                'shujuzhouqi': str(ar[0]),
                'diqu': str(ar[1]),
                'name': str(ar[2]),
                # WIS任务量
                'renwuliang': int(ar[3]),
                # 采集品
                'wiscj_caijipin': int(ar[4]),
                # 非采集
                'wiscj_feicaiji': int(ar[5]),
                # 常规任务量
                'jcrw_changguirenwu': int(ar[6]),
                # 新品采集 总量
                'xpcj_zongliang': int(ar[7]),
                # 麒麟
                'jcrw_qilin': int(ar[8]),
                # 麒麟量
                'qlcjl_hegeshuliang': int(ar[9]),

            })
    data['list'] = (list(c))
    return JsonResponse(data)


# 周期表后台数据
def zhouqibiao(request):
    data = {}
    c = []
    cursor1 = connection.cursor()
    cursor1.execute("SELECT * FROM `jx_zhouqibiao` where nianfen='2021'")
    raw = cursor1.fetchall()  # 读取所有
    for ar in raw:
        c.append({
            'nianfen': str(ar[1]),
            'pj': str(ar[2]),
            'pici': ar[3],
            'zhou': ar[4],
            'shujuzhouqi': ar[5],
            'kaohezhouqi': ar[6],
            'sj_kaishiri': ar[7],
            'sj_jiesuri': ar[8],
            'ke_kaishiri': ar[9],
            'ke_jiesuri': ar[10],
            'week': ar[11],
            'jidu': ar[12],
            'jiexiaoleixing': ar[13],
            'beizhu': ar[14],
            'gongzizhouqi': ar[15],
        })
    data['list'] = (list(c))
    return JsonResponse(data)


# STF处理情况表
def stfchulibiao(request):
    data = {}
    c = []
    cursor1 = connection.cursor()
    cursor1.execute(
        "SELECT endtime,yanghucanyu,diccfw3,caijixieru,feicaixieru,bunengxieru,tiaomahuichuan,buyizhi,bubiaozhun,shenhezhong,waiwen,qita FROM `w_stf_double_week` order by id asc")
    raw = cursor1.fetchall()  # 读取所有
    for ar in raw:
        c.append({
            'begintime': ar[0],  # product
            'yanghucanyu': ar[1],
            'diccfw3': ar[2],
            'caijixieru': ar[3],
            'feicaixieru': ar[4],
            'bunengxieru': ar[5],
            'tiaomahuichuan': ar[6],

            'buyizhi': ar[7],
            'bubiaozhun': ar[8],
            'shenhezhong': ar[9],
            'waiwen': ar[10],
            'qita': ar[11],

        })
    data['list'] = (list(c))
    return JsonResponse(data)


# 品類排名
def pinleicaijipaiming(request):
    data = {}
    c = []
    cursor1 = connection.cursor()
    cursor1.execute(
        "SELECT * FROM `w_category_yearcount` where  countdate>'2021-01-01'  and categoryid<899 order by id asc")
    raw = cursor1.fetchall()  # 读取所有
    for ar in raw:
        data = {}
        c.append({
            'categoryid': ar[1] + "-" + ar[2],  # product
            'reporttype': ar[3],
            'normalcount': ar[4],
            'wiscount': ar[5],
            'babycount': ar[6],
            'countdate': ar[7],
        })
    data['list'] = (list(c))
    return JsonResponse(data)


# 查询方法
def find(request):
    data = {}
    if request.GET.get('find'):
        find = request.GET.get('find')
        book = jx_jixiao.objects.filter(
            Q(name__icontains=find) | Q(quyu__icontains=find) | Q(diqu__icontains=find)).all().values()  # 获取值values放后面
    data['list'] = (list(book))
    return JsonResponse(data)


# 匹配率表
def pipeilvbiao(request):
    data = {}
    c = []
    cursor1 = connection.cursor()
    cursor1.execute("SELECT pci,hhp_matching,btp_matching,bbp_matching,kz_xiangzhenyangben,online_matching FROM `w_work_matching`")
    raw = cursor1.fetchall()  # 读取所有
    for ar in raw:
        c.append({
            'pci': str(ar[0]),
            'hhp_matching': str(ar[1]),
            'btp_matching': str(ar[2]),
            'bbp_matching': str(ar[3]),
            'kz_xiangzhenyangben': str(ar[4]),
            'online_matching': str(ar[5]),
        })
    data['list'] = (list(c))
    return JsonResponse(data)


def test(request):
    tup1 = ('physics', 'chemistry', 1997, 2000);
    tup2 = (1, 2, 3, 4, 5, 6, 7);

    print("tup1[0]: ", tup1[0])
    print("tup2[1:5]: ", tup2[1:5])
    return HttpResponse()


def sjqr_tiaozheng(request):
    data = {}
    if request.GET.get('jx'):
        id = request.GET.get('id')
        jx = request.GET.get('jx')
        book = jx_jixiao.objects.filter(Q(id__icontains=id)).update(sjqr_tiaozheng=jx)
        book2 = jx_jixiao.objects.all().values()
    data['list'] = (list(book2))
    return JsonResponse(data)


def writeFile(filePath, file):
    with open(filePath, "wb") as f:
        if file.multiple_chunks():
            for content in file.chunks():
                f.write(content)
        else:
            data = file.read()  ###.decode('utf-8')
            f.write(data)


def uploadfile(request):
    tup1 = ('physics', 'chemistry', 1997, 2000);
    tup2 = (1, 2, 3, 4, 5, 6, 7);

    print("tup1[0]: ", tup1[0])
    print("tup2[1:5]: ", tup2[1:5])
    return HttpResponse()


def j_mission_list(request):
    data = {}
    c = []
    if request.POST.get('upmc'):
        upmc = request.POST.get('upmc')
        qx = request.POST.get('qx')
        name = request.POST.get('name')
        cursor1 = connection.cursor()
        cursor1.execute(
            "SELECT * FROM `j_mission_up` where renwumingcheng='" + upmc + "' and querenren ='" + name + "'")
        raw = cursor1.fetchall()  # 读取所有
        for ar in raw:
            c.append({
                'id': str(ar[0]),
                'tiaoma': str(ar[1]),
                'miaoshu': str(ar[2]),
            })
        data['list'] = (list(c))
    return JsonResponse(data)


def tubiao_cons12(request):
    data = {}
    c = []
    cursor1 = connection.cursor()
    cursor1.execute("SELECT * FROM `tubiao_cons12` order by id desc")
    raw = cursor1.fetchall()  # 读取所有
    for ar in raw:
        c.append({
            'id': str(ar[0]),
            'diqu': str(ar[1]),
            'chengshi': str(ar[2]),
            'xingming': str(ar[3]),
            'changgui': str(ar[4]),
            'wis': str(ar[5]),
            'qilin': str(ar[6]),
            'fankui': str(ar[7]),
            'caijipin': str(ar[8]),
            'feicaijipin': str(ar[9]),
            'zongji': str(ar[10]),
        })
    data['list'] = (list(c))
    return JsonResponse(data)


def tubiao_cons12_xialakuang(request):
    data = {}
    c = []
    cursor1 = connection.cursor()
    if request.GET.get('diqu'):
        diqu = request.GET.get('diqu')
        cursor1.execute("SELECT * FROM `tubiao_cons12` where diqu='" + diqu + "' order by id desc")
        raw = cursor1.fetchall()  # 读取所有
        for ar in raw:
            c.append({
                'id': str(ar[0]),
                'diqu': str(ar[1]),
                'chengshi': str(ar[2]),
                'xingming': str(ar[3]),
                'changgui': str(ar[4]),
                'wis': str(ar[5]),
                'qilin': str(ar[6]),
                'fankui': str(ar[7]),
                'caijipin': str(ar[8]),
                'feicaijipin': str(ar[9]),
                'zongji': str(ar[10]),
            })
        data['list'] = (list(c))
    return JsonResponse(data)


# 表13
def tubiao_cons13(request):
    data = {}
    c = []
    cursor1 = connection.cursor()
    cursor1.execute("SELECT wisxinpincaijishuliang,qi,pci,zhouqi FROM `w_week_info` order by id asc")
    raw = cursor1.fetchall()  # 读取所有

    for ar in raw:
        if ar[3][-1] == "5":
            zhouqi = 5
        else:
            zhouqi = 4

        c.append({
            'wis': str(ar[0]),
            'riqi': str(ar[1]),
            'pci': str(ar[2]),
            'zhouqi': zhouqi,
        })
    data['list'] = (list(c))
    return JsonResponse(data)


# 2020年会 03表
def nianhui_03(request):
    data = {}
    c = []
    cursor1 = connection.cursor()
    if request.GET.get('diqu'):
        diqu = request.GET.get('diqu')
        cursor1.execute("SELECT * FROM `nianhui_03` where diqu='" + diqu + "' order by id asc")
        raw = cursor1.fetchall()  # 读取所有

        for ar in raw:
            c.append({
                'id': str(ar[0]),
                'diqu': str(ar[1]),
                'chengshi': str(ar[2]),
                'yiqueren': str(ar[3]),
                'kehupinpai': str(ar[4]),
                'zhongdianpinpai': str(ar[5]),
                'qita': str(ar[6]),
                'zongshu': str(ar[7]),
                'caijipinlv': str(ar[8]),
                'feicaijipinlv': str(ar[9]),
            })
        data['list'] = (list(c))
    return JsonResponse(data)


def excel_daochu(request):
    data = {}
    c = []
    cc = {}
    data2 = []
    i = 1
    if request.GET.get('mc'):
        mc = request.GET.get('mc')
        cursor1 = connection.cursor()
        cursor1.execute("SELECT * FROM `j_mission_up` where renwumingcheng='" + mc + "' order by id asc ")
        raw = cursor1.fetchall()
    # 创建工作簿
    wb = xlwt.Workbook(encoding='utf-8')
    sheet = wb.add_sheet('order-sheet')
    # 写入文件标题
    if raw:
        # 创建工作薄
        sheet.write(0, 0, "id")
        sheet.write(0, 1, u"tiaoma")
        sheet.write(0, 2, u"miaoshu")
        sheet.write(0, 3, u"querenshuoming")
        sheet.write(0, 4, u"beizhu")
        sheet.write(0, 5, u"time")
        sheet.write(0, 6, u"renwumingcheng")
        sheet.write(0, 7, u"zhuangtai")
        sheet.write(0, 8, u"querenren")
        sheet.write(0, 9, u"imgurl")
        sheet.write(0, 10, u"querentime")
        sheet.write(0, 11, u"houimage")
        # 写入数据
        excel_row = 1
        for obj in raw:
            sheet.write(excel_row, 0, obj[0])
            sheet.write(excel_row, 1, obj[1])
            sheet.write(excel_row, 2, obj[2])
            sheet.write(excel_row, 3, obj[3])
            sheet.write(excel_row, 4, obj[4])
            sheet.write(excel_row, 5, obj[5])
            sheet.write(excel_row, 6, obj[6])
            sheet.write(excel_row, 7, obj[7])
            sheet.write(excel_row, 8, obj[8])
            # 变形 #1判断是否为空 如果不为空 拆分
            if not obj[9] is None:
                L = obj[9]
                s1 = L.split(',')
                for index, x in enumerate(s1):
                    # 1-10
                    sheet.write(excel_row + index, 9, s1[index])
                count = index
            else:
                sheet.write(excel_row, 9, "空")
                count = 0
            sheet.write(excel_row, 10, obj[10])
            sheet.write(excel_row, 11, obj[11])
            excel_row = excel_row + count + 1
            # print(excel_row)

            # 检测文件是够存在
        ###########################以下为正确代码
        # os.path.exists判断括号里的文件是否存在的意思，括号内的可以是文件路径。
        exist_file = os.path.exists("./upload/test.xls")
        if exist_file:
            os.remove(r"./upload/test.xls")
        wb.save(r"./upload/test.xls")
        # BytesIO操作二进制数据
        sio = BytesIO()
        wb.save(sio)
        # seek()方法用于移动文件读取指针到指定位置
        sio.seek(0)
        response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=./upload/test.xls'
        response.write(sio.getvalue())
    return HttpResponse()

def excel_daochu2(request):
    data = {}
    c = []
    cc = {}
    data2 = []
    i = 1
    if request.GET.get('mc'):
        mc = request.GET.get('mc')
        cursor1 = connection.cursor()
        cursor1.execute("SELECT * FROM `mission_up` where renwumingcheng='" + mc + "' order by id asc ")
        raw = cursor1.fetchall()
    # 创建工作簿
    wb = xlwt.Workbook(encoding='utf-8')
    sheet = wb.add_sheet('order-sheet')
    # 写入文件标题
    if raw:
        # 创建工作薄
        sheet.write(0, 0, "id")
        sheet.write(0, 1, u"tiaoma")
        sheet.write(0, 2, u"miaoshu")
        sheet.write(0, 3, u"querenshuoming")
        sheet.write(0, 4, u"beizhu")
        sheet.write(0, 5, u"time")
        sheet.write(0, 6, u"renwumingcheng")
        sheet.write(0, 7, u"zhuangtai")
        sheet.write(0, 8, u"querenren")
        sheet.write(0, 9, u"imgurl")
        sheet.write(0, 10, u"querentime")
        sheet.write(0, 11, u"houimage")
        # 写入数据
        excel_row = 1
        for obj in raw:
            sheet.write(excel_row, 0, obj[0])
            sheet.write(excel_row, 1, obj[1])
            sheet.write(excel_row, 2, obj[2])
            sheet.write(excel_row, 3, obj[3])
            sheet.write(excel_row, 4, obj[4])
            sheet.write(excel_row, 5, obj[5])
            sheet.write(excel_row, 6, obj[6])
            sheet.write(excel_row, 7, obj[7])
            sheet.write(excel_row, 8, obj[8])
            # 变形 #1判断是否为空 如果不为空 拆分
            if not obj[9] is None:
                L = obj[9]
                s1 = L.split(',')
                for index, x in enumerate(s1):
                    # 1-10
                    sheet.write(excel_row + index, 9, s1[index])
                count = index
            else:
                sheet.write(excel_row, 9, "空")
                count = 0
            sheet.write(excel_row, 10, obj[10])
            sheet.write(excel_row, 11, obj[11])
            excel_row = excel_row + count + 1
            # print(excel_row)

            # 检测文件是够存在
        ###########################以下为正确代码
        # os.path.exists判断括号里的文件是否存在的意思，括号内的可以是文件路径。
        exist_file = os.path.exists(r"./upload/test.xls")
        if exist_file:
            os.remove(r"./upload/test.xls")
        wb.save(r"./upload/test.xls")
        # BytesIO操作二进制数据
        sio = BytesIO()
        wb.save(sio)
        # seek()方法用于移动文件读取指针到指定位置
        sio.seek(0)
        response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=./upload/test.xls'
        response.write(sio.getvalue())
    return HttpResponse()

def mission_find(request):
    c = []
    data = {}
    cursor1 = connection.cursor()
    if request.GET.get('renwumingcheng'):
        renwumingcheng = request.GET.get('renwumingcheng')
        tiaoma = request.GET.get('tiaoma')
        cursor1.execute(
            "SELECT * FROM `j_mission_up` where renwumingcheng='" + renwumingcheng + "' and tiaoma='" + tiaoma + "'  or renwumingcheng='" + renwumingcheng + "' and  querenren ='" + tiaoma + "' order by id asc")
        raw = cursor1.fetchall()  # 读取所有
        for ar in raw:
            c.append({
                'id': str(ar[0]),
                'tiaoma': str(ar[1]),
                'miaoshu': str(ar[2]),
                'querenshuoming': str(ar[3]),
                'beizhu': str(ar[4]),
                'time': str(ar[5]),
                'rewumingcheng': str(ar[6]),
                'zhuangtai': str(ar[7]),
                'querenren': str(ar[8]),
                'imgurl': str(ar[9]),
                'querentime': str(ar[10]),
                'houimage': str(ar[11]),
            })
        data['list'] = (list(c))
    return JsonResponse(data)


# 任务列表 使用状态
def mission_zhuangtai(request):
    data = {}
    if request.GET.get('beizhu'):
        id = request.GET.get('id')
        beizhu = request.GET.get('beizhu')
        book = j_mission_up.objects.filter(Q(id__icontains=id)).update(beizhu=beizhu)
    return JsonResponse(data)


# 任务列表 使用状态
def geren_mission(request):
    c = []
    data = {}
    cursor1 = connection.cursor()
    cursor2 = connection.cursor()
    cursor3 = connection.cursor()
    cursor4 = connection.cursor()
    cursor5 = connection.cursor()
    if request.GET.get('name'):
        username = request.GET.get('name')
        cursor1.execute("SELECT * FROM `j_begin_mission` order by id desc")
        raw = cursor1.fetchall()
        for ar in raw:
            # 个人还剩余条数
            cursor2.execute("SELECT count(*) FROM `j_mission_up` where renwumingcheng='" + ar[
                2] + "' and querenren='" + username + "' and zhuangtai is null ")
            raw2 = cursor2.fetchone()
            # 总数
            cursor3.execute("SELECT count(*) FROM `j_mission_up` where renwumingcheng='" + ar[2] + "'")
            raw3 = cursor3.fetchone()
            # 已完成
            cursor4.execute(
                "SELECT count(*) FROM `j_mission_up` where renwumingcheng='" + ar[2] + "' and zhuangtai !=''")
            raw4 = cursor4.fetchone()
            # 已使用
            cursor5.execute("SELECT count(*) FROM `j_mission_up` where renwumingcheng='" + ar[2] + "' and beizhu='已使用'")
            raw5 = cursor5.fetchone()
            zhuangtainull = int(raw3[0]) - int(raw4[0])
            c.append({
                'renwuriqi': ar[1],
                'renwumingcheng': ar[2],
                'jiezhiriqi': ar[4],
                'faburen': ar[3],
                'totalcount': raw3[0],
                'finishedcount': raw4[0],
                'usedcount': raw5[0],
                'zhuangtainull': zhuangtainull,
                'gerenshu': raw2[0],
                'beizhu': ar[6],
            })
            data['list'] = (list(c))
    return JsonResponse(data)


# 2020年 年度新品采集
def nianduxinpincaiji(request):
    data = {}
    c = []
    cursor1 = connection.cursor()
    cursor1.execute("SELECT * FROM `w_work_year` order by id asc")
    raw = cursor1.fetchall()  # 读取所有
    for ar in raw:
        c.append({
            'id': str(ar[0]),
            'year': str(ar[1]),
            'normal': str(ar[2]),
            'wis': str(ar[3]),
            'ql': str(ar[4]),
            'intercept': str(ar[5]),
            'total': str(ar[6]),
        })
    data['list'] = (list(c))
    return JsonResponse(data)


# 2020年 区域非采占比
def quyufeicaizhanbi(request):
    data = {}
    c = []
    cursor1 = connection.cursor()
    cursor1.execute("SELECT id,quyu,caijizhanbi FROM `w_region_commit`order by id desc  limit 8 ")
    raw = cursor1.fetchall()  # 读取所有
    for ar in raw:
        zhanbi = ar[2]
        c.append({
            'id': str(ar[0]),
            'quyu': str(ar[1]),
            'caijizhanbi': zhanbi,
        })
    data['list'] = (list(c))
    return JsonResponse(data)


# 2020年 每日自动处理数据
def meirizidongchulishuju(request):
    data = {}
    c = []
    cursor1 = connection.cursor()
    cursor1.execute("SELECT id,dealdate,stfcount,interceptcount,unmatchcount FROM `w_count_log`order by id asc ")
    raw = cursor1.fetchall()  # 读取所有
    for ar in raw:
        c.append({
            'id': str(ar[0]),
            'dealdate': str(ar[1]),
            'stfcount': str(ar[2]),
            'interceptcount': str(ar[3]),
            'unmatchcount': str(ar[4]),
        })
    data['list'] = (list(c))
    return JsonResponse(data)


def defen(request):
    data = {}
    c = []
    cursor1 = connection.cursor()
    cursor1.execute("SELECT * FROM `j_defen` where pci='P4' order by defen desc ")
    raw = cursor1.fetchall()  # 读取所有
    for ar in raw:
        c.append({
            'id': str(ar[0]),
            'pci': str(ar[1]),
            'quyu': str(ar[2]),
            'chengshi': str(ar[3]),
            'name': str(ar[4]),
            'defen': str(ar[5]),
            'f1': str(ar[6]),
            'f2': str(ar[7]),
        })
    data['list'] = (list(c))
    return JsonResponse(data)


def defen_pci(request):
    if request.GET.get('pici'):
        pici = request.GET.get('pici')
        data = {}
        c = []
        cursor1 = connection.cursor()
        cursor1.execute("SELECT * FROM `j_defen` where pci='" + pici + "' order by defen desc ")
        raw = cursor1.fetchall()  # 读取所有
        for ar in raw:
            c.append({
                'id': str(ar[0]),
                'pci': str(ar[1]),
                'quyu': str(ar[2]),
                'chengshi': str(ar[3]),
                'name': str(ar[4]),
                'defen': str(ar[5]),
                'f1': str(ar[6]),
                'f2': str(ar[7]),
            })
        data['list'] = (list(c))
    return JsonResponse(data)


def kaoqin_ck(request):
    data = {}
    c = []
    name1 = str(request.GET.get('username'))
    qx = str(request.GET.get('qx'))
    time = str(request.GET.get('time'))
    if (qx == "1"):
        cursor1 = connection.cursor()
        cursor1.execute("SELECT * FROM `j_kaoqin` order by riqi desc ")
        raw = cursor1.fetchall()  # 读取所有
        for ar in raw:
            c.append({
                'id': str(ar[0]),
                'name': str(ar[1]),
                'riqi': str(ar[2]),
                'shijian': str(ar[3]),
                'waiqinjindian': str(ar[4]),
                'waiqinjiaotong': str(ar[5]),
                'qudaohecha': str(ar[6]),
                # 'bangongshitingliu': str(ar[7]),
                'canjiapeixun': str(ar[8]),
                'wisluru': str(ar[9]),
                'changguiluru': str(ar[10]),
                'weichashiluru': str(ar[11]),
                'stfshujuluru': str(ar[12]),
                'dianshangshuju': str(ar[13]),
                'qilinshuju': str(ar[14]),
                'qita': str(ar[15]),
                'beizhu': str(ar[16]),
                'sflr': str(ar[17]),
                'qitashuoming': str(ar[18]),
                'wislurushuliang': str(ar[19]),
                'changguilurushuliang': str(ar[20]),
                'weichashilurushuliang': str(ar[21]),
                'stfshujulurushuliang': str(ar[22]),
                'dianshangshujushuliang': str(ar[23]),
                'qingjiaqingkuang': str(ar[24]),
                'diqu': str(ar[25]),
                'quyu': str(ar[26]),
                'zongshu': str(ar[27]),
            })
    else:

        if (time == "1"):
            cursor1 = connection.cursor()
            cursor1.execute("SELECT * FROM `j_kaoqin` where name='" + name1 + "' order by riqi desc ")
            raw = cursor1.fetchall()  # 读取所有
            for ar in raw:
                c.append({
                    'id': str(ar[0]),
                    'name': str(ar[1]),
                    'riqi': str(ar[2]),
                    'shijian': str(ar[3]),
                    'waiqinjindian': str(ar[4]),
                    'waiqinjiaotong': str(ar[5]),
                    'qudaohecha': str(ar[6]),
                    # 'bangongshitingliu': str(ar[7]),
                    'canjiapeixun': str(ar[8]),
                    'wisluru': str(ar[9]),
                    'changguiluru': str(ar[10]),
                    'weichashiluru': str(ar[11]),
                    'stfshujuluru': str(ar[12]),
                    'dianshangshuju': str(ar[13]),
                    'qilinshuju': str(ar[14]),
                    'qita': str(ar[15]),
                    'beizhu': str(ar[16]),
                    'sflr': str(ar[17]),
                    'qitashuoming': str(ar[18]),
                    'wislurushuliang': str(ar[19]),
                    'changguilurushuliang': str(ar[20]),
                    'weichashilurushuliang': str(ar[21]),
                    'stfshujulurushuliang': str(ar[22]),
                    'dianshangshujushuliang': str(ar[23]),
                    'qingjiaqingkuang': str(ar[24]),
                    'diqu': str(ar[25]),
                    'quyu': str(ar[26]),
                    'zongshu': str(ar[27]),
                })
        else:
            print("地方2")
            cursor1 = connection.cursor()
            cursor1.execute(
                "SELECT * FROM `j_kaoqin` where name='" + name1 + "' and riqi='" + time + "'  order by riqi desc")
            raw = cursor1.fetchall()  # 读取所有
            for ar in raw:
                c.append({
                    'id': str(ar[0]),
                    'name': str(ar[1]),
                    'riqi': str(ar[2]),
                    'shijian': str(ar[3]),
                    'waiqinjindian': str(ar[4]),
                    'waiqinjiaotong': str(ar[5]),
                    'qudaohecha': str(ar[6]),
                    # 'bangongshitingliu': str(ar[7]),
                    'canjiapeixun': str(ar[8]),
                    'wisluru': str(ar[9]),
                    'changguiluru': str(ar[10]),
                    'weichashiluru': str(ar[11]),
                    'stfshujuluru': str(ar[12]),
                    'dianshangshuju': str(ar[13]),
                    'qilinshuju': str(ar[14]),
                    'qita': str(ar[15]),
                    'beizhu': str(ar[16]),
                    'sflr': str(ar[17]),
                    'qitashuoming': str(ar[18]),
                    'wislurushuliang': str(ar[19]),
                    'changguilurushuliang': str(ar[20]),
                    'weichashilurushuliang': str(ar[21]),
                    'stfshujulurushuliang': str(ar[22]),
                    'dianshangshujushuliang': str(ar[23]),
                    'qingjiaqingkuang': str(ar[24]),
                    'diqu': str(ar[25]),
                    'quyu': str(ar[26]),
                    'zongshu': str(ar[27]),
                })
    data['list'] = (list(c))
    return JsonResponse(data)


def kaoqin_ck2(request):
    data = {}
    c = []
    id = str(request.GET.get('id'))
    cursor1 = connection.cursor()
    cursor1.execute("SELECT * FROM `j_kaoqin` where id='" + id + "'  order by riqi desc")
    raw = cursor1.fetchall()  # 读取所有
    for ar in raw:
        c.append({
            'id': str(ar[0]),
            'name': str(ar[1]),
            'riqi': str(ar[2]),
            'shijian': str(ar[3]),
            'waiqinjindian': str(ar[4]),
            'waiqinjiaotong': str(ar[5]),
            'qudaohecha': str(ar[6]),
            'canjiapeixun': str(ar[8]),
            'wisluru': str(ar[9]),
            'changguiluru': str(ar[10]),
            'weichashiluru': str(ar[11]),
            'stfshujuluru': str(ar[12]),
            'dianshangshuju': str(ar[13]),
            'qilinshuju': str(ar[14]),
            'qita': str(ar[15]),
            'beizhu': str(ar[16]),
            'sflr': str(ar[17]),
            'qitashuoming': str(ar[18]),
            'wislurushuliang': str(ar[19]),
            'changguilurushuliang': str(ar[20]),
            'weichashilurushuliang': str(ar[21]),
            'stfshujulurushuliang': str(ar[22]),
            'dianshangshujushuliang': str(ar[23]),
            'qingjiaqingkuang': str(ar[24]),
            'diqu': str(ar[25]),
            'quyu': str(ar[26]),
            'zongshu': str(ar[27]),
        })
    data['list'] = (list(c))
    return JsonResponse(data)


def kaoqin(request):
    data = {}
    diqu = str(request.GET.get('diqu'))
    quyu = str(request.GET.get('quyu'))
    name1 = str(request.GET.get('name'))
    riqi = str(request.GET.get('riqi'))
    shijian = str(request.GET.get('shijian'))
    waiqinjindian = str(request.GET.get('waiqinjindian'))
    waiqinjiaotong = str(request.GET.get('waiqinjiaotong'))
    qudaohecha = str(request.GET.get('qudaohecha'))
    # bangongshitingliu = str(request.GET.get('bangongshitingliu'))
    canjiapeixun = str(request.GET.get('canjiapeixun'))
    wisluru = str(request.GET.get('wisluru'))
    changguiluru = str(request.GET.get('changguiluru'))
    weichashiluru = str(request.GET.get('weichashiluru'))
    stfshujuluru = str(request.GET.get('stfshujuluru'))
    dianshangshuju = str(request.GET.get('dianshangshuju'))
    qilinshuju = str(request.GET.get('qilinshuju'))
    qita = str(request.GET.get('qita'))
    beizhu = str(request.GET.get('beizhu'))

    qingjiaqingkuang = str(request.GET.get('qingjiaqingkuang'))
    qitashuoming = str(request.GET.get('qitashuoming'))
    wislurushuliang = str(request.GET.get('wislurushuliang'))
    changguilurushuliang = str(request.GET.get('changguilurushuliang'))
    weichashilurushuliang = str(request.GET.get('weichashilurushuliang'))
    stfshujulurushuliang = str(request.GET.get('stfshujulurushuliang'))
    dianshangshujushuliang = str(request.GET.get('dianshangshujushuliang'))

    if len(str(request.GET.get('waiqinjindian'))) == 0:
        waiqinjindian = 0
    if len(str(request.GET.get('waiqinjiaotong'))) == 0:
        waiqinjiaotong = 0
    if len(str(request.GET.get('canjiapeixun'))) == 0:
        canjiapeixun = 0
    if len(str(request.GET.get('qudaohecha'))) == 0:
        qudaohecha = 0
    if len(str(request.GET.get('wisluru'))) == 0:
        wisluru = 0
    if len(str(request.GET.get('changguiluru'))) == 0:
        changguiluru = 0
    if len(str(request.GET.get('weichashiluru'))) == 0:
        weichashiluru = 0
    if len(str(request.GET.get('stfshujuluru'))) == 0:
        stfshujuluru = 0
    if len(str(request.GET.get('dianshangshuju'))) == 0:
        dianshangshuju = 0
    if len(str(request.GET.get('qilinshuju'))) == 0:
        qilinshuju = 0

    # print(waiqinjindian)
    # print(waiqinjiaotong)
    # print(canjiapeixun)
    # print(qudaohecha)
    # print(wisluru)
    # print(changguiluru)
    # print(weichashiluru)
    # print(stfshujuluru)
    # print(dianshangshuju)
    # print(qilinshuju)
    zongshu2 = int(waiqinjindian) + int(waiqinjiaotong) + int(canjiapeixun) + int(qudaohecha) + int(wisluru) + int(
        changguiluru) + int(weichashiluru) + int(stfshujuluru) + int(dianshangshuju) + int(qilinshuju)

    cursor1 = connection.cursor()
    cursor1.execute(
        "INSERT INTO  j_kaoqin ("
        "zongshu,"
        "diqu,"
        "quyu,"
        "name,"
        "shijian,"
        "riqi,"
        "waiqinjindian,"
        "waiqinjiaotong,"
        "qudaohecha,"
        "canjiapeixun,"
        "wisluru,"
        "changguiluru,"
        "weichashiluru,"
        "stfshujuluru,"
        "dianshangshuju,"
        "qilinshuju,"
        "qita,"
        "beizhu,"
        "sflr,"
        "qingjiaqingkuang,"
        "qitashuoming,"
        "wislurushuliang,"
        "changguilurushuliang,"
        "weichashilurushuliang,"
        "stfshujulurushuliang,"
        "dianshangshujushuliang) VALUES('" + str(zongshu2) + "',"
                                                             "'" + diqu + "',"
                                                                          "'" + quyu + "',"
                                                                                       "'" + name1 + "',"
                                                                                                     "'" + shijian + "',"
                                                                                                                     "'" + riqi + "',"
                                                                                                                                  "'" + str(
            waiqinjindian) + "',"
                             "'" + str(waiqinjiaotong) + "',"
                                                         "'" + str(qudaohecha) + "',"
                                                                                 "'" + str(canjiapeixun) + "',"
                                                                                                           "'" + str(
            wisluru) + "',"
                       "'" + str(changguiluru) + "',"
                                                 "'" + str(weichashiluru) + "',"
                                                                            "'" + str(stfshujuluru) + "',"
                                                                                                      "'" + str(
            dianshangshuju) + "',"
                              "'" + str(qilinshuju) + "',"
                                                      "'" + qita + "','" + beizhu + "',1,'" + qingjiaqingkuang + "','" + qitashuoming + "','" + wislurushuliang + "','" + changguilurushuliang + "','" + weichashilurushuliang + "','" + stfshujulurushuliang + "','" + dianshangshujushuliang + "')")
    raw = cursor1.fetchall()  # 读取所有
    return HttpResponse()


def kaoqin_up(request):
    data = {}
    j_id = str(request.GET.get('id'))
    j_name1 = str(request.GET.get('username'))
    j_riqi = str(request.GET.get('riqi'))
    j_diqu = str(request.GET.get('diqu'))
    j_quyu = str(request.GET.get('quyu'))
    j_shijian = str(request.GET.get('shijian'))
    j_waiqinjindian = str(request.GET.get('waiqinjindian'))
    j_waiqinjiaotong = str(request.GET.get('waiqinjiaotong'))
    j_qudaohecha = str(request.GET.get('qudaohecha'))
    # j_bangongshitingliu = str(request.GET.get('bangongshitingliu'))
    j_canjiapeixun = str(request.GET.get('canjiapeixun'))
    j_wisluru = str(request.GET.get('wisluru'))
    j_changguiluru = str(request.GET.get('changguiluru'))
    j_weichashiluru = str(request.GET.get('weichashiluru'))
    j_stfshujuluru = str(request.GET.get('stfshujuluru'))
    j_dianshangshuju = str(request.GET.get('dianshangshuju'))
    j_qilinshuju = str(request.GET.get('qilinshuju'))
    j_qita = str(request.GET.get('qita'))
    j_beizhu = str(request.GET.get('beizhu'))
    j_qingjiaqingkuang = str(request.GET.get('qingjiaqingkuang'))
    j_qitashuoming = str(request.GET.get('qitashuoming'))
    j_wislurushuliang = str(request.GET.get('wislurushuliang'))
    j_changguilurushuliang = str(request.GET.get('changguilurushuliang'))
    j_weichashilurushuliang = str(request.GET.get('weichashilurushuliang'))
    j_stfshujulurushuliang = str(request.GET.get('stfshujulurushuliang'))
    j_dianshangshujushuliang = str(request.GET.get('dianshangshujushuliang'))

    if len(str(request.GET.get('waiqinjindian'))) == 0:
        j_waiqinjindian = 0
    if len(str(request.GET.get('waiqinjiaotong'))) == 0:
        j_waiqinjiaotong = 0
    if len(str(request.GET.get('canjiapeixun'))) == 0:
        j_canjiapeixun = 0
    if len(str(request.GET.get('qudaohecha'))) == 0:
        j_qudaohecha = 0
    if len(str(request.GET.get('wisluru'))) == 0:
        j_wisluru = 0
    if len(str(request.GET.get('changguiluru'))) == 0:
        j_changguiluru = 0
    if len(str(request.GET.get('weichashiluru'))) == 0:
        j_weichashiluru = 0
    if len(str(request.GET.get('stfshujuluru'))) == 0:
        j_stfshujuluru = 0
    if len(str(request.GET.get('dianshangshuju'))) == 0:
        j_dianshangshuju = 0
    if len(str(request.GET.get('qilinshuju'))) == 0:
        j_qilinshuju = 0
    # print(qilinshuju)
    zongshu2 = int(j_waiqinjindian) + int(j_waiqinjiaotong) + int(j_canjiapeixun) + int(j_qudaohecha) + int(
        j_wisluru) + int(
        j_changguiluru) + int(j_weichashiluru) + int(j_stfshujuluru) + int(j_dianshangshuju) + int(j_qilinshuju)

    # INSERT INTO 表名称 VALUES (值1, 值2,....)
    print(zongshu2)
    cursor1 = connection.cursor()
    cursor1.execute("UPDATE j_kaoqin SET "
                    "zongshu='" + str(zongshu2) + "',"
                                                  " waiqinjindian='" + j_waiqinjindian + "',"
                                                                                         "waiqinjiaotong='" + j_waiqinjiaotong + "',"
                                                                                                                                 "qudaohecha='" + j_qudaohecha + "',"
                                                                                                                                                                 "canjiapeixun='" + j_canjiapeixun + "',"
                                                                                                                                                                                                     "wisluru='" + j_wisluru + "',"
                                                                                                                                                                                                                               "changguiluru='" + j_changguiluru + "',"
                                                                                                                                                                                                                                                                   "weichashiluru='" + j_weichashiluru + "',"
                                                                                                                                                                                                                                                                                                         "stfshujuluru='" + j_stfshujuluru + "',"
                                                                                                                                                                                                                                                                                                                                             "dianshangshuju='" + j_dianshangshuju + "',"
                                                                                                                                                                                                                                                                                                                                                                                     "qilinshuju='" + j_qilinshuju + "',"
                                                                                                                                                                                                                                                                                                                                                                                                                     "qita='" + j_qita + "',"
                                                                                                                                                                                                                                                                                                                                                                                                                                         "beizhu='" + j_beizhu + "',"
                                                                                                                                                                                                                                                                                                                                                                                                                                                                 "qingjiaqingkuang='" + j_qingjiaqingkuang + "',"
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             "qitashuoming='" + j_qitashuoming + "',"
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 "wislurushuliang='" + j_wislurushuliang + "',"
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           "changguilurushuliang='" + j_changguilurushuliang + "',"
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               "weichashilurushuliang='" + j_weichashilurushuliang + "',"
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     "stfshujulurushuliang='" + j_stfshujulurushuliang + "',"
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         "dianshangshujushuliang='" + j_dianshangshujushuliang + "' where name='" + j_name1 + "' and riqi='" + j_riqi + "' and id='" + j_id + "'")
    raw = cursor1.fetchall()  # 读取所有
    return HttpResponse()


def kaoqin_del(request):
    j_id = str(request.GET.get('id'))
    cursor1 = connection.cursor()
    cursor1.execute("DELETE FROM j_kaoqin WHERE id = '" + j_id + "'")
    raw = cursor1.fetchall()  # 读取所有
    return HttpResponse()


def kaoqin_ck_riqi(request):
    data = {}
    c = []
    d = []
    e = []
    j_riqi = str(request.GET.get('beginTime'))

    cursor2 = connection.cursor()
    cursor2.execute("SELECT * FROM `user` where qx=4  order by id desc ")
    raw2 = cursor2.fetchall()  # 读取所有
    for ar in raw2:
        c.append(ar[1])

    cursor1 = connection.cursor()
    cursor1.execute("SELECT * FROM `j_kaoqin` where riqi='" + j_riqi + "' order by id desc ")
    raw = cursor1.fetchall()  # 读取所有
    for arr in raw:
        d.append(arr[1])

    for i in c:
        if i not in d:
            e.append({'name': i})

    data['list'] = (list(e))

    return JsonResponse(data)


def w_stf_categoryid_count(request):
    data = {}
    c = []
    e = []
    cursor0 = connection.cursor()
    cursor0.execute("SELECT count(DISTINCT(categoryid)) FROM `w_stf_categoryid_count` ")
    count0 = cursor0.fetchone()

    cursor3 = connection.cursor()
    cursor3.execute("SELECT  DISTINCT(endtime) FROM `w_stf_categoryid_count` order by endtime asc")
    row3 = cursor3.fetchall()

    for datevalue in row3:

        cursor1 = connection.cursor()
        cursor1.execute(
            "SELECT * FROM `w_stf_categoryid_count` where endtime='" + (datevalue[0]) + "' order by endtime asc")
        row = cursor1.fetchall()

        d = []
        for ar in row:
            d.append({
                'categoryid': ar[3],
                'countz': ar[4],
                'datevalue': ar[2]
            })

        c.append(d)

    c.append({'end': {'countzs': count0, 'countdate': row3, 'zhouqi': row}})
    data['list'] = (list(c))
    return JsonResponse(data)


def excel_map_daochu(request):
    data = {}
    c = []
    cc = {}
    data2 = []
    i = 1
    if request.GET.get('mc'):
        mc = request.GET.get('mc')
    cursor1 = connection.cursor()
    cursor1.execute("SELECT * FROM `map` where name='" + mc + "' order by id asc ")
    list_obj = cursor1.fetchall()

    # 创建工作簿
    wb = xlwt.Workbook(encoding='utf-8')

    sheet = wb.add_sheet('order-sheet')

    # 写入文件标题
    if list_obj:
        # 创建工作薄
        sheet.write(0, 0, "id")
        sheet.write(0, 1, u"X")
        sheet.write(0, 2, u"y")
        sheet.write(0, 3, u"beign")
        sheet.write(0, 4, u"end")
        sheet.write(0, 5, u"name")
        sheet.write(0, 6, u"time")
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

            print(excel_row)

            # 检测文件是够存在
        ###########################以下为正确代码
        # os.path.exists判断括号里的文件是否存在的意思，括号内的可以是文件路径。
        exist_file = os.path.exists(r"./upload/地区.xls")
        if exist_file:
            os.remove(r"./upload/地区.xls")
        wb.save(r"./upload/地区.xls")
        # BytesIO操作二进制数据
        sio = BytesIO()
        wb.save(sio)
        # seek()方法用于移动文件读取指针到指定位置
        sio.seek(0)
        response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=./upload/地区.xls'
        response.write(sio.getvalue())
    return response


def handle_upload_file(file, filename):
    path = r'./upload/'  # 图片保存路径
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + filename, 'wb') as destination:
        for chunk in file.chunks():
            # print(chunk)
            destination.write(chunk)
    return filename


def left_img_add(request):
    img_url = ''
    path = ''

    if request.method == "POST":
        img_url = handle_upload_file(request.FILES.get('file'), str(request.FILES['file']))
        msg = {}
        msg['msg'] = '上传成功'
        msg['success'] = True
        msg['path'] = img_url

        file_type = msg['path'].split(".")[1]
        try:
            path = './upload/' + msg['path']
            print(path)
            data = xlrd.open_workbook(path)
            table = data.sheet_by_name(u'Sheet1')  # 通过名称获取
            nrows = table.nrows
            cursor = connection.cursor()
            cursor.execute("truncate table ctr.4171")
            row = cursor.fetchall()
            for i in (range(nrows)):
                table.row_values(i)
                cursor.execute("INSERT INTO ctr.4171 (barcode) VALUES ('{}')".format(table.row_values(i)[0]))
                row = cursor.fetchall()
        except IOError:
            print("Error: 没有找到文件或读取文件失败")
    return HttpResponse()


def left_add(request):
    try:
        data = {}
        user = str(request.GET.get('user'))
        neirong = str(request.GET.get('neirong'))
        biaoti = str(request.GET.get('biaoti'))
        zhonglei = str(request.GET.get('zhonglei'))
        riqi = str(request.GET.get('riqi'))
        tuisong = str(request.GET.get('tuisong'))

        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO j_left_add (user,neirong,biaoti,zhonglei,riqi,tuisong) VALUES ('{}','{}','{}','{}','{}','{}')".format(
                user, neirong, biaoti, zhonglei, riqi, tuisong))
        row = cursor.fetchall()
    except Exception as err:
        print("报错终止")
        print(Exception)
    return HttpResponse()


def left_add_ck(request):
    data = {}
    c = []
    d = []
    # if request.GET.get('id'):
    #     id = request.GET.get('id')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM `j_left_add`  order by id desc")
    row = cursor.fetchall()
    for ar in row:
        d.append({
            'id': ar[0],
            'biaoti': ar[1],
            'zhonglei': ar[2],
            'riqi': ar[3],
            'tuisong': ar[4],
            'neirong': ar[5],
            'user': ar[6],
        })

    data['list'] = (list(d))
    return JsonResponse(data)


def left_add_ck_nr(request):
    data = {}
    c = []
    d = []
    id = str(request.GET.get('id'))

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM `j_left_add` where id=" + id + "  order by id desc")
    row = cursor.fetchall()
    for ar in row:
        d.append({
            'id': ar[0],
            'biaoti': ar[1],
            'zhonglei': ar[2],
            'riqi': ar[3],
            'tuisong': ar[4],
            'neirong': ar[5],
            'user': ar[6],
        })

    c.append(d)
    data['list'] = (list(c))
    return JsonResponse(data)


def left_del(request):
    j_id = str(request.GET.get('id'))
    cursor1 = connection.cursor()
    cursor1.execute("DELETE FROM j_left_add WHERE id = '" + j_id + "'")
    raw = cursor1.fetchall()  # 读取所有
    return HttpResponse()


# ---------------------------迁移任务------------------------------

# 迁移功能---------------------------------------------------------
def qianyi(request):
    data = {}
    c = []
    cursor1 = connection.cursor()
    cursor1.execute("select * FROM begin_mission order by id desc")
    raw = cursor1.fetchall()  # 读取所有
    for ar in raw:
        # 总量
        cursor2 = connection.cursor()
        cursor2.execute("SELECT count(*) as total FROM mission_up where renwumingcheng='" + ar[2] + "'")
        raw2 = cursor2.fetchone()  # 读取所有
        # 已完成
        cursor3 = connection.cursor()
        cursor3.execute("SELECT count(*) as total FROM mission_up where renwumingcheng='" + ar[2] + "' and zhuangtai=2")
        raw3 = cursor3.fetchone()  # 读取所有
        # 未完成
        raw4 = int(raw2[0]) - int(raw3[0])
        c.append({
            'id': str(ar[0]),
            'renwuriqi': str(ar[1]),
            'renwumingcheng': str(ar[2]),
            'faburen': str(ar[3]),
            'jiezhiriqi': str(ar[4]),
            'zhuangtai': str(ar[5]),
            'beizhu': str(ar[6]),
            'totalcount': raw2[0],
            'finishedcount': raw3[0],
            'zhuangtainull': raw4
        })
    data['list'] = (list(c))
    return JsonResponse(data)


def qianyi_find(request):
    data = {}
    c = []
    upmc = str(request.GET.get('upmc'))
    tiaoma = str(request.GET.get('tiaoma'))
    all=str(request.GET.get('all'))
    queren=str(request.GET.get('queren'))
    weiqueren=str(request.GET.get('weiqueren'))

    if all=='1':
        cursor1 = connection.cursor()
        cursor1.execute(
            "select * FROM mission_up where  renwumingcheng='" + upmc + "' order by id desc")
        raw = cursor1.fetchall()  # 读取所有
    elif queren=='1':
        cursor1 = connection.cursor()
        cursor1.execute(
            "select * FROM mission_up where  renwumingcheng='" + upmc + "' and zhuangtai='2' order by id desc")
        raw = cursor1.fetchall()  # 读取所有
    elif weiqueren=='2':
        cursor1 = connection.cursor()
        cursor1.execute(
            "select * FROM mission_up where  renwumingcheng='" + upmc + "' and zhuangtai='1' order by id desc")
        raw = cursor1.fetchall()  # 读取所有
    else:
        cursor1 = connection.cursor()
        cursor1.execute(
            "select * FROM mission_up where  tiaoma='" + tiaoma + "' and renwumingcheng='" + upmc + "' or querenren='"+tiaoma+"'  and renwumingcheng='" + upmc + "' order by id desc")
        raw = cursor1.fetchall()  # 读取所有
    for ar in raw:
        c.append({
            'id': str(ar[0]),
            'tiaoma': str(ar[1]),
            'miaoshu': str(ar[2]),
            'querenshuoming': str(ar[3]),
            'beizhu': str(ar[4]),
            'time': str(ar[5]),
            'renwumingcheng': str(ar[6]),
            'zhuangtai': str(ar[7]),
            'querenren': str(ar[8]),
            'querenren_chengshi': str(ar[9]),
            'querentime': str(ar[10]),
            'jiage': str(ar[11]),
            'baozhuangxingshi': str(ar[12]),
        })
    data['list'] = (list(c))
    return JsonResponse(data)


# 迁移功能展示
def qianyi_show(request):
    data = {}
    c = []
    upmc = str(request.GET.get('upmc'))
    name=str(request.GET.get('name'))
    if request.GET.get('name'):

        cursor1 = connection.cursor()
        cursor1.execute("select * FROM mission_up where renwumingcheng='" + upmc + "' and querenren='"+name+"' order by id desc")
        raw = cursor1.fetchall()  # 读取所有
        for ar in raw:
            c.append({
                'id': str(ar[0]),
                'tiaoma': str(ar[1]),
                'miaoshu': str(ar[2]),
                'querenshuoming': str(ar[3]),
                'beizhu': str(ar[4]),
                'time': str(ar[5]),
                'renwumingcheng': str(ar[6]),
                'zhuangtai': str(ar[7]),
                'querenren': str(ar[8]),
                'querenren_chengshi': str(ar[9]),
                'querentime': str(ar[10]),
                'jiage': str(ar[11]),
                'baozhuangxingshi': str(ar[12]),
            })
    else:
        cursor1 = connection.cursor()
        cursor1.execute("select * FROM mission_up where renwumingcheng='" + upmc + "' order by id desc")
        raw = cursor1.fetchall()  # 读取所有
        for ar in raw:
            c.append({
                'id': str(ar[0]),
                'tiaoma': str(ar[1]),
                'miaoshu': str(ar[2]),
                'querenshuoming': str(ar[3]),
                'beizhu': str(ar[4]),
                'time': str(ar[5]),
                'renwumingcheng': str(ar[6]),
                'zhuangtai': str(ar[7]),
                'querenren': str(ar[8]),
                'querenren_chengshi': str(ar[9]),
                'querentime': str(ar[10]),
                'jiage': str(ar[11]),
                'baozhuangxingshi': str(ar[12]),
            })
    data['list'] = (list(c))
    return JsonResponse(data)


def qianyi_zt(request):
    data = {}
    c = []
    if request.GET.get('id'):
        id = request.GET.get('id')
        diqu = request.GET.get('diqu')
        user = request.GET.get('user')
        upmc = request.GET.get('upmc')
        beizhu = request.GET.get('beizhu')
        time = datetime.datetime.now().strftime('%Y-%m-%d')
        cursor1 = connection.cursor()
        cursor1.execute(
            "UPDATE mission_up SET zhuangtai=2,querenren='" + str(user) + "',querenren_chengshi='" + str(
                diqu) + "',querentime='" + time + "',beizhu='" + beizhu + "' WHERE id='" + id + "'")
        raw = cursor1.fetchall()  # 读取所有

        cursor1 = connection.cursor()
        cursor1.execute("select * FROM mission_up where renwumingcheng='" + upmc + "' order by id desc")
        raw = cursor1.fetchall()  # 读取所有
        for ar in raw:
            c.append({
                'id': str(ar[0]),
                'tiaoma': str(ar[1]),
                'miaoshu': str(ar[2]),
                'querenshuoming': str(ar[3]),
                'beizhu': str(ar[4]),
                'time': str(ar[5]),
                'renwumingcheng': str(ar[6]),
                'zhuangtai': str(ar[7]),
                'querenren': str(ar[8]),
                'querenren_chengshi': str(ar[9]),
                'querentime': str(ar[10]),
                'jiage': str(ar[11]),
                'baozhuangxingshi': str(ar[12]),
            })
        data['list'] = (list(c))
    return JsonResponse(data)


def qianyi_user(request):
    data = {}
    c = []
    cursor1 = connection.cursor()
    cursor1.execute("select * FROM user where qx='4' order by id desc")
    raw = cursor1.fetchall()  # 读取所有
    for ar in raw:
        c.append({
            'id': str(ar[0]),
            'name': str(ar[1]),
        })
    data['list'] = (list(c))
    return JsonResponse(data)


# 数据分解 上传及导出
def qianyi_upload(request):
    img_url = ''
    data = {}
    path = ''
    c = []
    data2 = []
    data3 = []
    ht_msg = ''
    if request.method == "POST":
        img_url = handle_upload_file(request.FILES.get('file'), str(request.FILES['file']))
        msg = {}
        msg['msg'] = '上传成功'
        msg['success'] = True
        msg['path'] = img_url
        path = './upload/' + msg['path']
        data = xlrd.open_workbook(path)
        table = data.sheet_by_name(u'Sheet1')  # 通过名称获取
        nrows = table.nrows
        for j in (range(nrows)):
            table.row_values(j)

            cursor2 = connection.cursor()
            cursor2.execute(
                "INSERT INTO mission_up (tiaoma,miaoshu,querenshuoming,beizhu,renwumingcheng,zhuangtai) "
                "VALUES ('{}','{}','{}','{}','{}','{}')".format(
                    table.row_values(j)[1],
                    table.row_values(j)[2],
                    table.row_values(j)[3],
                    table.row_values(j)[4],
                    table.row_values(j)[5],
                    int(table.row_values(j)[6]),
                ))
            row = cursor2.fetchall()
    return HttpResponse()


def qianyi_begin(request):
    try:
        riqi = str(request.POST.get('riqi'))
        renwumingcheng = str(request.POST.get('renwumingcheng'))
        faburen = str(request.POST.get('faburen'))
        jiezhiriqi = str(request.POST.get('jiezhiriqi'))
        beizhu = str(request.POST.get('beizhu'))
        fenpei = str(request.POST.get('fenpei'))
        print(fenpei)
        cursor2 = connection.cursor()
        cursor2.execute(
            "INSERT INTO begin_mission (renwuriqi,renwumingcheng,faburen,jiezhiriqi,zhuangtai,beizhu,fenpei,upmc) "
            "VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')".format(
                riqi, renwumingcheng, faburen, jiezhiriqi, 'on', beizhu, fenpei, renwumingcheng
            ))
        row = cursor2.fetchall()
    except Exception as err:
        print(err)
        print("报错终止")
        print(Exception)
    return HttpResponse()


# 迁移功能结束---------------------------------------------------------------
# 通知------------------------------------------------------------
def tongzhi(request):
    diqu = str(request.GET.get('diqu'))
    name = str(request.GET.get('name'))
    top = str(request.GET.get('top'))
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    cursor1 = connection.cursor()
    cursor1.execute(
        "INSERT INTO tongzhi (name,tongzhibiaoti,diqu,time,zt) VALUES ('{}','{}','{}','{}','{}')".format(name, top,
                                                                                                         diqu, date,
                                                                                                         '1'))
    raw = cursor1.fetchall()  # 读取所有

    return HttpResponse()


def tongzhi_ck(request):
    data = {}
    c = []
    name = str(request.GET.get('name'))
    riqi = str(request.GET.get('riqi'))
    cursor1 = connection.cursor()
    cursor1.execute("select * from tongzhi where time>'" + riqi + "' and name='" + name + "'")
    raw = cursor1.fetchall()  # 读取所有
    for ar in raw:
        c.append({
            'id': ar[0],
            'name': ar[1],
            'tongzhibiaoti': ar[2],
            'diqu': ar[3],
            'time': ar[4],
            'zt': ar[5],
        })
    data['list'] = (list(c))
    return JsonResponse(data)


# 通知结束---------------------------------------------------------

# 加点------------------------------------------------------------
def jiadian(request):
    data = {}
    c = []
    name = str(request.GET.get('name'))
    if request.GET.get('name'):
        cursor1 = connection.cursor()
        cursor1.execute("select * from jd where dd='"+name+"' order by time desc")
        raw = cursor1.fetchall()  # 读取所有
        for ar in raw:
            c.append({
                'id': ar[0],
                'pc': ar[1],
                'time': ar[2],
                'tj': ar[3],
                'qy': ar[4],
                'bsc': ar[5],
                'ydcs': ar[6],
                'jtbh': ar[7],
                'tm': ar[8],
                'fwyxm': ar[9],
                'fwybh': ar[10],
                'jb': ar[11],
                'pic': ar[12],
                'pldm': ar[13],
                'dd': ar[14],
            })
        data['list'] = (list(c))
    else:
        cursor1 = connection.cursor()
        cursor1.execute("select * from jd order by time desc")
        raw = cursor1.fetchall()  # 读取所有
        for ar in raw:
            c.append({
                'id': ar[0],
                'pc': ar[1],
                'time': ar[2],
                'tj': ar[3],
                'qy': ar[4],
                'bsc': ar[5],
                'ydcs': ar[6],
                'jtbh': ar[7],
                'tm': ar[8],
                'fwyxm': ar[9],
                'fwybh': ar[10],
                'jb': ar[11],
                'pic': ar[12],
                'pldm': ar[13],
                'dd': ar[14],
            })
        data['list'] = (list(c))
    return JsonResponse(data)


def jiadian_tj(request):
    try:
        pc = str(request.GET.get('pc'))
        time = str(request.GET.get('time'))
        tj = str(request.GET.get('tj'))
        qy = str(request.GET.get('qy'))
        bsc = str(request.GET.get('bsc'))
        ydcs = str(request.GET.get('ydcs'))
        jtbh = str(request.GET.get('jtbh'))
        tm = str(request.GET.get('tm'))
        fwyxm = str(request.GET.get('fwyxm'))
        fwybh = str(request.GET.get('fwybh'))
        jb = str(request.GET.get('jb'))
        pic = str(request.GET.get('pic'))
        pldm = str(request.GET.get('pldm'))
        dd = str(request.GET.get('dd'))

        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO jd (pc,tj,qy,bsc,ydcs,jtbh,tm,fwyxm,fwybh,jb,pic,pldm,dd) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                pc, tj, qy, bsc, ydcs, jtbh, tm, fwyxm, fwybh, jb, pic, pldm, dd))
        row = cursor.fetchall()
    except Exception as err:
        print("报错终止")
        print(Exception)
    return HttpResponse()


def jiadian_xg(request):
    data = {}
    c = []
    try:
        id = str(request.GET.get('id'))
        pc = str(request.GET.get('pc'))
        tj = str(request.GET.get('tj'))
        qy = str(request.GET.get('qy'))
        bsc = str(request.GET.get('bsc'))
        ydcs = str(request.GET.get('ydcs'))
        jtbh = str(request.GET.get('jtbh'))
        tm = str(request.GET.get('tm'))
        fwyxm = str(request.GET.get('fwyxm'))
        fwybh = str(request.GET.get('fwybh'))
        jb = str(request.GET.get('jb'))
        pic = str(request.GET.get('pic'))
        pldm = str(request.GET.get('pldm'))
        dd = str(request.GET.get('dd'))

        # print(pc)
        # print(tj)
        # print(qy)
        # print(bsc)
        # print(ydcs)
        # print(jtbh)
        # print(tm)
        # print(fwyxm)
        # print(fwybh)
        # print(jb)
        # print(pic)
        # print(pldm)
        # print(dd)
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE jd SET pc='" + (pc) + "',tj='" + (tj) + "',qy='" + (qy) + "',bsc='" + (bsc) + "',ydcs='" + (
                ydcs) + "',jtbh='" + (jtbh) + "',tm='" + (tm) + "',fwyxm='" + (fwyxm) + "',fwybh='" + (
                fwybh) + "', jb='" + (jb) + "',pic='" + (jb) + "',pic ='" + (pic) + "',pldm ='" + (pldm) + "',dd ='" + (
                dd) + "' WHERE id='" + (id) + "'")
        row = cursor.fetchall()
        cursor1 = connection.cursor()
        cursor1.execute("select * from jd order by time desc")
        raw = cursor1.fetchall()  # 读取所有
        for ar in raw:
            c.append({
                'id': ar[0],
                'pc': ar[1],
                'time': ar[2],
                'tj': ar[3],
                'qy': ar[4],
                'bsc': ar[5],
                'ydcs': ar[6],
                'jtbh': ar[7],
                'tm': ar[8],
                'fwyxm': ar[9],
                'fwybh': ar[10],
                'jb': ar[11],
                'pic': ar[12],
                'pldm': ar[13],
                'dd': ar[14],
            })
        data['list'] = (list(c))
    except Exception as err:
        print("报错终止")
        print(Exception)
    return JsonResponse(data)


def jiadian_del(request):
    id = str(request.GET.get('id'))
    cursor = connection.cursor()
    cursor.execute("DELETE FROM jd where id='" + id + "'")
    row = cursor.fetchall()
    return HttpResponse()


def jiadian_find(request):
    c = []
    data = {}
    begin = str(request.GET.get('begin'))
    finish = str(request.GET.get('finish'))
    key = str(request.GET.get('key'))
    if request.GET.get('key'):
        cursor = connection.cursor()
        cursor.execute("select * from jd where jtbh='" + key + "' or tm='" + key + "' order by time desc")
        raw = cursor.fetchall()
        for ar in raw:
            c.append({
                'id': ar[0],
                'pc': ar[1],
                'time': ar[2],
                'tj': ar[3],
                'qy': ar[4],
                'bsc': ar[5],
                'ydcs': ar[6],
                'jtbh': ar[7],
                'tm': ar[8],
                'fwyxm': ar[9],
                'fwybh': ar[10],
                'jb': ar[11],
                'pic': ar[12],
                'pldm': ar[13],
                'dd': ar[14],
            })

        data['list'] = (list(c))

    if request.GET.get('begin'):
        cursor = connection.cursor()
        cursor.execute(
            "select * from jd where time>='" + str(begin) + "' and time<='" + str(finish) + "' order by time desc")
        raw = cursor.fetchall()
        for ar in raw:
            c.append({
                'id': ar[0],
                'pc': ar[1],
                'time': ar[2],
                'tj': ar[3],
                'qy': ar[4],
                'bsc': ar[5],
                'ydcs': ar[6],
                'jtbh': ar[7],
                'tm': ar[8],
                'fwyxm': ar[9],
                'fwybh': ar[10],
                'jb': ar[11],
                'pic': ar[12],
                'pldm': ar[13],
                'dd': ar[14],
            })

        data['list'] = (list(c))
    return JsonResponse(data)


def jiadian_daochu(request):
    data = {}
    c = []
    cc = {}
    data2 = []
    i = 1

    begin = request.GET.get('begin')
    finish = request.GET.get('finish')
    cursor1 = connection.cursor()
    cursor1.execute("SELECT * FROM `jd` where time>'" + begin + "' and time<='" + finish + "' order by id asc ")
    list_obj = cursor1.fetchall()

    # 创建工作簿
    wb = xlwt.Workbook(encoding='utf-8')

    sheet = wb.add_sheet('order-sheet')

    # 写入文件标题
    if list_obj:
        # 创建工作薄
        sheet.write(0, 0, u"id")
        sheet.write(0, 1, u"period")
        sheet.write(0, 2, u"时间")
        sheet.write(0, 3, u"途径")
        sheet.write(0, 4, u"区域")
        sheet.write(0, 5, u"办事处")
        sheet.write(0, 6, u"样点城市")
        sheet.write(0, 7, u"家庭编号")
        sheet.write(0, 8, u"条码")
        sheet.write(0, 9, u"访问员姓名")
        sheet.write(0, 10, u"访问员编号")
        sheet.write(0, 11, u"级别")
        sheet.write(0, 12, u"频次")
        sheet.write(0, 13, u"品类代码")
        sheet.write(0, 14, u"督导")
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
            sheet.write(excel_row, 7, obj[7])
            sheet.write(excel_row, 8, obj[8])
            sheet.write(excel_row, 9, obj[9])
            sheet.write(excel_row, 10, obj[10])
            sheet.write(excel_row, 11, obj[11])
            sheet.write(excel_row, 12, obj[12])
            sheet.write(excel_row, 13, obj[13])
            sheet.write(excel_row, 14, obj[14])
            count = 0
            excel_row = excel_row + count + 1

            # 检测文件是够存在
        ###########################以下为正确代码
        # os.path.exists判断括号里的文件是否存在的意思，括号内的可以是文件路径。
        exist_file = os.path.exists(r"./upload/加点.xls")
        if exist_file:
            os.remove(r"./upload/加点.xls")
        wb.save(r"./upload/加点.xls")
        # BytesIO操作二进制数据
        sio = BytesIO()
        wb.save(sio)
        # seek()方法用于移动文件读取指针到指定位置
        sio.seek(0)
        response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=./upload/加点.xls'
        response.write(sio.getvalue())

    return response


# 加点结束---------------------------------------------------------

# GS1查询---------------------------------------------------------
def GS1(request):
    c = []
    data = {}
    host = 'https://ali-barcode.showapi.com'
    path = '/barcode'
    method = 'GET'
    appcode = '1fb56623de844f1bb2de46c28a2db5cf'
    cursor = connection.cursor()
    cursor.execute("select * from ctr.4171 order by id desc")
    raw = cursor.fetchall()
    for ar in (raw):
        print(ar[1])
        querys = 'code=' + ar[1]
        bodys = {}
        url = host + path + '?' + querys
        try:
            request = urllib.request.Request(url)
            request.add_header('Authorization', 'APPCODE ' + appcode)
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            response = urllib.request.urlopen(request, context=ctx)
            content = response.read().decode('utf8')
            count = (json.loads(content))
            print(count['showapi_res_body']['goodsName'])
            code = count['showapi_res_body']['code']
            goodsName = count['showapi_res_body']['goodsName']
            manuName = count['showapi_res_body']['manuName']
            spec = count['showapi_res_body']['spec']
            price = count['showapi_res_body']['price']
            trademark = count['showapi_res_body']['trademark']
            img = count['showapi_res_body']['img']
            imgList = count['showapi_res_body']['imgList']
            ycg = count['showapi_res_body']['ycg']
            note = count['showapi_res_body']['note']
            cursor = connection.cursor()
            cursor.execute(
                "insert into GS1_rukubiao(code,goodsName,manuName,spec,price,trademark,img,imgList,ycg,note) values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                    code, goodsName, manuName, spec, price, trademark, img, imgList, ycg, note))
            raw = cursor.fetchall()

        except IOError:
            print("报错了")
    return HttpResponse()


# GS1查询结束------------------------------------------------------
# 三周绩效---------------------------------------------------------
def sanzhoujixiao(request):
    data = {}
    c = []
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sanzhoujixiao where time >'2021-01-01' order by id desc")
    raw = cursor.fetchall()
    for ar in (raw):
        c.append({
            'name': ar[1],
            'pci': ar[2],
            'pcizhou': ar[3],
            'queren': ar[4],
            'time': ar[5],
            'diqu': ar[6],
        })
    data['list'] = (list(c))
    return JsonResponse(data)


def sanzhoujixiao_add(request):
    try:
        data = {}
        name = str(request.POST.get('name'))
        pci = str(request.POST.get('pci'))
        pcizhou = str(request.POST.get('zhou'))
        diqu = str(request.POST.get('diqu'))
        cursor = connection.cursor()
        cursor.execute(
            "insert into sanzhoujixiao(name,pci,pcizhou,diqu) values ('{}','{}','{}','{}')".format(
                name, pci, pcizhou, diqu))
        row = cursor.fetchall()
    except Exception as err:
        print(err)
        print("报错终止")
        print(Exception)
    return HttpResponse()


def sanzhoujixiao_find(request):
    data = {}
    c = []
    pci = str(request.GET.get('pci2'))
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sanzhoujixiao where time >'2022-01-01' and pci='" + pci + "' order by id desc")
    raw = cursor.fetchall()
    for ar in (raw):
        c.append({
            'name': ar[1],
            'pci': ar[2],
            'pcizhou': ar[3],
            'queren': ar[4],
            'time': ar[5],
            'diqu': ar[6],
        })
    data['list'] = (list(c))
    return JsonResponse(data)


# 三周绩效结束------------------------------------------------------
# dicc指导--------------------------------------------------------
def zhidao_dl_add(request):
    region = str(request.GET.get('region'))
    name = str(request.GET.get('dl'))
    cursor = connection.cursor()
    cursor.execute("INSERT INTO dicc_dl (name,dl,xl) VALUES ('{}','{}','{}')".format(name, region, 0))
    raw = cursor.fetchall()
    return HttpResponse()


def zhidao_xl_add(request):
    region = str(request.GET.get('val'))
    name = str(request.GET.get('xl'))
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM dicc_dl where name='"+region+"'")
    raw = cursor.fetchall()
    xl=raw[0][2]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO dicc_xl (xl,name) VALUES ('{}','{}')".format(xl, name))
    raw = cursor.fetchall()
    return HttpResponse()


def zhidao_del(request):
    id = str(request.GET.get('id'))
    dl = str(request.GET.get('dl'))
    name=str(request.GET.get('name'))
    if (id == 'dl'):
        cursor = connection.cursor()
        cursor.execute("delete from dicc_dl where dl='" + dl + "'")
        raw = cursor.fetchall()
    else:
        cursor = connection.cursor()
        cursor.execute("delete from dicc_xl where name='" + name + "'")
        raw = cursor.fetchall()
    return HttpResponse()


def zhidao_dl(request):
    data = {}
    c = []
    d = []
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM dicc_dl  order by dl asc")
    raw = cursor.fetchall()
    for ar in (raw):
        cursor2 = connection.cursor()
        cursor2.execute("SELECT * FROM dicc_xl where xl='" + ar[2] + "' order by name asc")
        raw2 = cursor2.fetchall()
        e = []
        for ar2 in raw2:
            e.append({'label': ar2[2], 'type': 'menu'})

        d.append({'label': ar[1], 'dlpx': ar[2], 'children': e})

    data['list'] = (list(d))

    return JsonResponse(data)


def zhidao_nr(request):
    data = {}
    c = []
    xl = str(request.GET.get('xl'))
    dl = str(request.GET.get('dl'))
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM dicc_nr where xl='" + xl + "'")
    raw = cursor.fetchall()
    if (raw):
        for ar in (raw):
            c.append({
                'dl': ar[1],
                'textarea': ar[2],
                'xl': ar[3],
                'time': ar[4],
                'datetime': ar[5],
            })
    else:
        c = []
    data['list'] = (list(c))
    return JsonResponse(data)


def zhidao_ty(request):
    data = {}
    c = []
    xl = str(request.GET.get('xl'))
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM dicc_ty order by id asc")
    raw = cursor.fetchall()
    for ar in (raw):
        c.append({
            'mc': ar[1],
            'nr': ar[2],
            'px': ar[3],
            'time': ar[4],
            'up_time': ar[5],
        })
    data['list'] = (list(c))
    return JsonResponse(data)


def zhidao_up(request):
    try:
        data = {}
        c = []
        xl = str(request.GET.get('xl'))
        nr = str(request.GET.get('nr'))
        dl = str(request.GET.get('dl'))
        time = datetime.datetime.now().strftime('%Y-%m-%d')

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM dicc_nr where xl='" + xl + "'")
        raw = cursor.fetchall()
        if (raw):
            cursor = connection.cursor()
            cursor.execute("UPDATE dicc_nr SET textarea='" + (nr) + "' WHERE xl='" + xl + "'")
            row = cursor.fetchall()

            cursor2 = connection.cursor()
            cursor2.execute("SELECT * FROM dicc_nr where xl='" + xl + "'")
            raw2 = cursor2.fetchall()
            for ar in (raw2):
                c.append({
                    'dl': ar[1],
                    'textarea': ar[2],
                    'xl': ar[3],
                    'time': ar[4],
                    'datetime': ar[5],
                })
            data['list'] = (list(c))
        else:

            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO dicc_nr (dl,xl,textarea,datetime) VALUES ('{}','{}','{}','{}')".format(dl, xl, nr, time))
            row = cursor.fetchall()
    except Exception as err:
        print("报错终止")
        print(Exception)
    return JsonResponse(data)


def dicc_img_add(request):
    img_url = ''
    path = ''

    img_url = handle_upload_file2(request.FILES.get('file'), str(request.FILES['file']))
    msg = {}
    msg['msg'] = '上传成功'
    msg['success'] = True
    msg['path'] = img_url
    path = './upload/' + msg['path']
    print(path)
    return HttpResponse(json.dumps(msg))


def handle_upload_file2(file, filename):
    path = r'./upload/'  # 图片保存路径
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + filename, 'wb') as destination:
        for chunk in file.chunks():
            # print(chunk)
            destination.write(chunk)
    return filename


# dicc指导结束-----------------------------------------------------

# 数据分解---------------------------------------------------------
def j_shujufenjie(request):
    data = {}
    c = []
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM fj order by id desc")
    raw = cursor.fetchall()
    for ar in (raw):
        c.append({
            'id': ar[0],
            'qc': ar[1],
            'fj': ar[2],
            'pl': ar[3],
            'bh': ar[4],
        })
    data['list'] = (list(c))
    return JsonResponse(data)


# 数据分解 上传及导出
def sj_upload(request):
    img_url = ''
    data = {}
    path = ''
    c = []
    data2 = []
    data3 = []
    ht_msg = ''
    if request.method == "POST":
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
        cursor.execute("truncate table sjfj")

        for j in (range(nrows)):
            table.row_values(j)
            qc = ''
            lianjie = ''
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
            try:
                cursor.execute(
                    "INSERT INTO sjfj (tiaoma,miaoshu,pinpai,jiage,xingming,queren,qc,lianjie,bh,pinpaiku) "
                    "VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                        table.row_values(j)[0],
                        table.row_values(j)[1],
                        table.row_values(j)[2],
                        table.row_values(j)[3],
                        table.row_values(j)[4],
                        table.row_values(j)[5],
                        qc,
                        lianjie,
                        table.row_values(j)[8],
                        table.row_values(j)[9],
                    ))
                row = cursor.fetchall()
                ht_msg = ''
            except Exception:
                ht_msg = '123'
                break

        cursor1 = connection.cursor()
        cursor1.execute("SELECT * FROM `sjfj` order by id asc ")
        list_obj = cursor1.fetchall()

        # 创建工作簿
        wb = xlwt.Workbook(encoding='utf-8')

        sheet = wb.add_sheet('order-sheet')

        # 写入文件标题
        if list_obj:
            # 创建工作薄
            sheet.write(0, 0, u"id")
            sheet.write(0, 1, u"tiaoma")
            sheet.write(0, 2, u"miaoshu")
            sheet.write(0, 3, u"pinpai")
            sheet.write(0, 4, u"jiage")
            sheet.write(0, 5, u"xingming")
            sheet.write(0, 6, u"queren")
            sheet.write(0, 7, u"qc")
            sheet.write(0, 8, u"lianjie")
            sheet.write(0, 9, u"bh")
            sheet.write(0, 10, u"pinpaiku")
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
                sheet.write(excel_row, 7, obj[7])
                sheet.write(excel_row, 8, obj[8])
                sheet.write(excel_row, 9, obj[9])
                sheet.write(excel_row, 10, obj[10])
                count = 0
                excel_row = excel_row + count + 1

                # 检测文件是够存在
            ###########################以下为正确代码
            # os.path.exists判断括号里的文件是否存在的意思，括号内的可以是文件路径。
            exist_file = os.path.exists(r"./upload/数据分解.xls")
            if exist_file:
                os.remove(r"./upload/数据分解.xls")
            wb.save(r"./upload/数据分解.xls")
            # BytesIO操作二进制数据
            sio = BytesIO()
            wb.save(sio)
            # seek()方法用于移动文件读取指针到指定位置
            sio.seek(0)
            response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=./upload/数据分解.xls'
            response.write(sio.getvalue())

    return HttpResponse(ht_msg)


def sj_add(request):
    qc = str(request.GET.get('qc'))
    fj = str(request.GET.get('fj'))
    pl = str(request.GET.get('pl'))

    data = {}
    c = []
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM fj where qc='" + qc + "' order by id desc")
    raw = cursor.fetchall()

    cursor.execute("INSERT INTO fj (qc,fj,pl) VALUES ('{}','{}','{}')".format(qc, fj, int(pl)))
    raw = cursor.fetchall()

    cursor.execute("SELECT * FROM fj order by id desc")
    raw = cursor.fetchall()
    for ar in (raw):
        c.append({
            'id': ar[0],
            'qc': ar[1],
            'fj': ar[2],
            'pl': ar[3],
            'bh': ar[4],
        })

    data['list'] = (list(c))

    return JsonResponse(data)


def sj_del(request):
    id = str(request.GET.get('id'))
    data = {}
    c = []
    cursor = connection.cursor()
    cursor.execute("DELETE FROM fj where id='" + id + "' ")
    raw = cursor.fetchall()
    return HttpResponse()


# 厂商码分解
def j_cj(request):
    data = {}
    c = []
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM fj_gongsi order by id desc")
    raw = cursor.fetchall()
    for ar in (raw):
        c.append({
            'id': ar[0],
            'mc': ar[1],
        })
    data['list'] = (list(c))
    return JsonResponse(data)


def cs_upload(request):
    img_url = ''
    data = {}
    path = ''
    c = []
    data2 = []
    data3 = []
    ht_msg = ''
    if request.method == "POST":
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
        cursor.execute("truncate table sjfj_gs")

        for j in (range(nrows)):
            table.row_values(j)
            bh = ''
            cursor2 = connection.cursor()
            cursor2.execute("SELECT * FROM fj_gongsi order by id desc")
            raw = cursor2.fetchall()
            for i in raw:
                print(table.row_values(j)[2])
                val = i[1] in table.row_values(j)[2]
                if val == True:
                    bh = '包含关键字'
                    break
                else:
                    bh = '不包含'
            try:
                cursor.execute(
                    "INSERT INTO sjfj_gs (tiaoma,mc,bh) "
                    "VALUES ('{}','{}','{}')".format(
                        table.row_values(j)[1],
                        table.row_values(j)[2],
                        bh,
                    ))
                row = cursor.fetchall()
                ht_msg = ''
            except Exception:
                ht_msg = '123'
                break

        cursor1 = connection.cursor()
        cursor1.execute("SELECT * FROM `sjfj_gs` order by id asc ")
        list_obj = cursor1.fetchall()

        # 创建工作簿
        wb = xlwt.Workbook(encoding='utf-8')

        sheet = wb.add_sheet('order-sheet')

        # 写入文件标题
        if list_obj:
            # 创建工作薄
            sheet.write(0, 0, u"id")
            sheet.write(0, 1, u"tiaoma")
            sheet.write(0, 2, u"mc")
            sheet.write(0, 3, u"bh")
            # 写入数据
            excel_row = 1
            for obj in list_obj:
                sheet.write(excel_row, 0, obj[0])
                sheet.write(excel_row, 1, obj[1])
                sheet.write(excel_row, 2, obj[2])
                sheet.write(excel_row, 3, obj[3])
                count = 0
                excel_row = excel_row + count + 1

                # 检测文件是够存在
            ###########################以下为正确代码
            # os.path.exists判断括号里的文件是否存在的意思，括号内的可以是文件路径。
            exist_file = os.path.exists(r"./upload/厂家数据分解.xls")
            if exist_file:
                os.remove(r"./upload/厂家数据分解.xls")
            wb.save(r"./upload/厂家数据分解.xls")
            # BytesIO操作二进制数据
            sio = BytesIO()
            wb.save(sio)
            # seek()方法用于移动文件读取指针到指定位置
            sio.seek(0)
            response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=./upload/厂家数据分解.xls'
            response.write(sio.getvalue())

    return HttpResponse(ht_msg)


def cs_del(request):
    id = str(request.GET.get('id'))
    data = {}
    c = []
    cursor = connection.cursor()
    cursor.execute("DELETE FROM fj_gs where id='" + id + "' ")
    raw = cursor.fetchall()
    return HttpResponse()


# 数据分解结束------------------------------------------------------
# 考核开始---------------------------------------------------------
def kaohe_add(request):
    timu = str(request.GET.get('timu'))
    a = str(request.GET.get('a'))
    b = str(request.GET.get('b'))
    cc = str(request.GET.get('c'))
    d = str(request.GET.get('d'))
    e = str(request.GET.get('e'))
    f = str(request.GET.get('f'))
    g = str(request.GET.get('g'))
    h = str(request.GET.get('h'))
    daan = str(request.GET.get('daan'))
    data = {}
    c = []
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO kaoshi_timu_gth (timu,A,B,C,D,E,F,G,H,daan) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
            timu, a, b, cc, d, e, f, g, h, daan))
    raw = cursor.fetchall()

    cursor = connection.cursor()
    cursor.execute("SELECT * from kaoshi_timu_gth order by id desc")
    raw = cursor.fetchall()
    for ar in (raw):
        c.append({
            'id': ar[0],
            'timu': ar[1],
            'A': ar[2],
            'B': ar[3],
            'C': ar[4],
            'D': ar[5],
            'E': ar[6],
            'F': ar[7],
            'G': ar[8],
            'H': ar[9],
            'daan': ar[12],
        })
    data['list'] = (list(c))
    return JsonResponse(data)


def kaohe_ck(request):
    data = {}
    c = []
    cursor = connection.cursor()
    cursor.execute("SELECT * from kaoshi_timu_gth order by id desc")
    raw = cursor.fetchall()
    for ar in (raw):
        c.append({
            'id': ar[0],
            'timu': ar[1],
            'A': ar[2],
            'B': ar[3],
            'C': ar[4],
            'D': ar[5],
            'E': ar[6],
            'F': ar[7],
            'G': ar[8],
            'H': ar[9],
            'daan': ar[12],
        })
    data['list'] = (list(c))
    return JsonResponse(data)


def kaohe_ck2(request):
    data = {}
    c = []
    cursor = connection.cursor()
    cursor.execute("SELECT * from kaoshi_timu_gth ORDER BY RAND() LIMIT 0,20")
    #cursor.execute("SELECT * from kaoshi_timu_gth")
    raw = cursor.fetchall()
    for ar in (raw):
        c.append({
            'id': ar[0],
            'timu': ar[1],
            'A': ar[2],
            'B': ar[3],
            'C': ar[4],
            'D': ar[5],
            'E': ar[6],
            'F': ar[7],
            'G': ar[8],
            'H': ar[9],
            'daan': ar[12],
        })
    data['list'] = (list(c))
    return JsonResponse(data)


def kaohe_xg(request):
    data = {}
    c = []

    id = str(request.GET.get('id'))
    timu = str(request.GET.get('timu'))
    a = str(request.GET.get('a'))
    b = str(request.GET.get('b'))
    cc = str(request.GET.get('c'))
    d = str(request.GET.get('d'))
    e = str(request.GET.get('e'))
    f = str(request.GET.get('f'))
    g = str(request.GET.get('g'))
    h = str(request.GET.get('h'))
    daan = str(request.GET.get('daan'))

    cursor = connection.cursor()
    cursor.execute(
        "UPDATE kaoshi_timu_gth SET timu='" + timu + "',A='" + a + "',B='" + b + "',C='" + cc + "',D='" + d + "',E='" + e + "',F='" + f + "',G='" + g + "',H='" + h + "',daan='" + daan + "' WHERE id='" + id + "'")
    raw = cursor.fetchall()

    cursor = connection.cursor()
    cursor.execute("SELECT * from kaoshi_timu_gth order by id desc")
    raw = cursor.fetchall()
    for ar in (raw):
        c.append({
            'id': ar[0],
            'timu': ar[1],
            'A': ar[2],
            'B': ar[3],
            'C': ar[4],
            'D': ar[5],
            'E': ar[6],
            'F': ar[7],
            'G': ar[8],
            'H': ar[9],
            'daan': ar[12],
        })
    data['list'] = (list(c))
    return JsonResponse(data)


def kaohe_del(request):
    data = {}
    c = []
    id = str(request.GET.get('id'))
    cursor = connection.cursor()
    cursor.execute("DELETE FROM kaoshi_timu_gth WHERE id = '" + id + "'")
    raw = cursor.fetchall()

    cursor = connection.cursor()
    cursor.execute("SELECT * from kaoshi_timu_gth order by id desc")
    raw = cursor.fetchall()
    for ar in (raw):
        c.append({
            'id': ar[0],
            'timu': ar[1],
            'A': ar[2],
            'B': ar[3],
            'C': ar[4],
            'D': ar[5],
            'E': ar[6],
            'F': ar[7],
            'G': ar[8],
            'H': ar[9],
            'daan': ar[12],
        })
    data['list'] = (list(c))
    return JsonResponse(data)


def kaohe_jg(request):
    user = str(request.GET.get('user'))
    diqu = str(request.GET.get('diqu'))
    jieguo = str(request.GET.get('jieguo'))
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO kaoshi_gth (text,user,jieguo) VALUES ('{}','{}','{}')".format(diqu, user, jieguo))
    raw = cursor.fetchall()

    return HttpResponse()


def kaohe_tg(request):
    data = {}
    c = []
    cursor = connection.cursor()
    cursor.execute("SELECT * from kaoshi_gth where time>'2022-05-25' order by id desc")
    raw = cursor.fetchall()
    for ar in (raw):
        c.append({
            'user': ar[2]
        })
    data['list'] = (list(c))
    return JsonResponse(data)


# 考核结束---------------------------------------------------------


# 培训开始---------------------------------------------------------
def peixun_ck(request):
    data = {}
    c = []
    cursor = connection.cursor()
    cursor.execute("SELECT * from peixun order by id desc")
    raw = cursor.fetchall()
    for ar in (raw):
        c.append({
            'id': ar[0],
            'pci': ar[1],
            'pinlei': ar[2],
            'pinleimingcheng': ar[3],
            'pinleifuzeren': ar[4],
            'zhubiaoti': ar[5],
            'pinleijieshao': ar[6],
        })
    data['list'] = (list(c))
    return JsonResponse(data)


def peixun_xg(request):
    data = {}
    c = []

    id = str(request.GET.get('id'))
    pci = str(request.GET.get('pci'))
    pinleimingcheng = str(request.GET.get('pinleimingcheng'))
    pinleifuzeren = str(request.GET.get('pinleifuzeren'))
    zhubiaoti = str(request.GET.get('zhubiaoti'))
    pinleijieshao = str(request.GET.get('pinleijieshao'))

    cursor = connection.cursor()
    cursor.execute(
        "UPDATE peixun SET pci='" + pci + "',pinleimingcheng='" + pinleimingcheng + "',pinleifuzeren='" + pinleifuzeren + "',zhubiaoti='" + zhubiaoti + "',pinleijieshao='" + pinleijieshao + "' WHERE id='" + id + "'")
    raw = cursor.fetchall()

    cursor = connection.cursor()
    cursor.execute("SELECT * from peixun order by id desc")
    raw = cursor.fetchall()
    for ar in (raw):
        c.append({
            'id': ar[0],
            'pci': ar[1],
            'pinlei': ar[2],
            'pinleimingcheng': ar[3],
            'pinleifuzeren': ar[4],
            'zhubiaoti': ar[5],
            'pinleijieshao': ar[6],
            'zipinlei': ar[7],
        })
    data['list'] = (list(c))
    return JsonResponse(data)


def peixun_del(request):
    data = {}
    c = []
    id = str(request.GET.get('id'))
    cursor = connection.cursor()
    cursor.execute("DELETE FROM peixun WHERE id = '" + id + "'")
    raw = cursor.fetchall()

    cursor = connection.cursor()
    cursor.execute("SELECT * from peixun order by id desc")
    raw = cursor.fetchall()
    for ar in (raw):
        c.append({
            'id': ar[0],
            'pci': ar[1],
            'pinlei': ar[2],
            'pinleimingcheng': ar[3],
            'pinleifuzeren': ar[4],
            'zhubiaoti': ar[5],
            'pinleijieshao': ar[6],
        })
    data['list'] = (list(c))
    return JsonResponse(data)


def peixun_add(request):
    data = {}
    c = []
    pci = str(request.GET.get('pci'))
    pinleimingcheng = str(request.GET.get('pinleimingcheng'))
    pinleifuzeren = str(request.GET.get('pinleifuzeren'))
    zhubiaoti = str(request.GET.get('zhubiaoti'))
    pinleijieshao = str(request.GET.get('pinleijieshao'))
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO kaoshi_timu (pci,pinleimingcheng,pinleifuzeren,zhubiaoti,pinleijieshao) VALUES ('{}','{}','{}','{}','{}')".format(
            pci, pinleimingcheng, pinleifuzeren, zhubiaoti, pinleijieshao))
    raw = cursor.fetchall()
    return HttpResponse()
# 培训结束---------------------------------------------------------
