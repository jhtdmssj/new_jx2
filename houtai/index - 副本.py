# # -*- coding: utf-8 -*-
from django.db import connection
from django.http import JsonResponse, HttpResponse
from houtai.models import User, JxZhouqibiao,jx_jixiao,jx_jixiao_all,w_work_info_tmp
from django.db.models import Q
import datetime
import time
import json

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

            return JsonResponse({'code': 2, 'message': '登录成功', 'user': response1})
    else:
        return JsonResponse({'code': 1, 'message': '用户名或密码错误，请重新输入'})
    return



#后台跑库 已经忘记干嘛用的了（- -！）
def houtai_jx(request):
    #第一步 jx_jixiao表里的内容全部删除
    jx_jixiao.objects.all().delete()

    data = {}
    c=[]
    renwul=''
    sz=''
    #判断是否有查询
    if request.GET.get('pici'):
        pici = request.GET.get('pici')
        week = request.GET.get('week')
    else:
        #pici 当前月的批次 week当前月的周
        pici = '1'
        week = '2'
    #创建链接
    cursor1 = connection.cursor()
    caiji = connection.cursor()
    feicaiji=connection.cursor()
    xp_zl=connection.cursor()
    xp_kh=connection.cursor()
    xp_zd=connection.cursor()
    xp_ql=connection.cursor()
    fkl_wis=connection.cursor()
    fkl_wis_2=connection.cursor()
    fkl_cg=connection.cursor()
    fkl_cg_2=connection.cursor()
    fkl_ql=connection.cursor()
    xiujia=connection.cursor()
    fkl_ql_zl=connection.cursor()
    mydata=connection.cursor()



    #基础表
    cursor1.execute("SELECT * FROM `jx_zhouqibiao`,`user`,`jx_zhourenwu` WHERE USER.qx = '4' AND jx_zhourenwu.user_id=user.id and pici='1' and zhou='2'")
    raw =cursor1.fetchall()  # 读取所有
    #获取当前系统日期
    dqdate = datetime.datetime.now().strftime('%Y-%m-%d')
    print(dqdate)

    for ar in raw:
        #如果当前日期小于等于 绩效日期 就停止
        if dqdate <= ar[9] :
           break
        else :

            #周期2020P1-1
            zhouqi = str(ar[1])+str(ar[2])+str(ar[3])+"-"+str(ar[4])
            #ar[4] 批次是周
            if ar[4]=='1':
                renwul=round(int(ar[28])*0.2)
            elif ar[4]=='2':
                renwul=round(int(ar[28])*0.28)
            elif ar[4]=='3':
                renwul=round(int(ar[28])*0.32)
            elif ar[4]=='4':
                renwul=round(int(ar[28])*0.2)
            elif ar[4]=='5':
                renwul=round(int(ar[28])*0.24)




            #ar[9]是kaishiri
            #ar[10]是jiesuri
            #ar[18]是人名
            #ar[23]是地区

            # wis采集
            caiji.execute("SELECT COUNT( DISTINCT id) FROM  w_commodity WHERE submittime >= '"+ar[9]+"' AND submittime <= '"+ar[10]+"' AND datatype != 1 AND categoryid != '9001' and categoryid < '899' AND realname = '"+ar[18]+"' and cityname = '"+ar[23]+"' AND status != 4;")
            raw2 = caiji.fetchone()  # 读取所有
            # wis非采集
            feicaiji.execute("SELECT COUNT( DISTINCT id ) FROM w_commodity WHERE datatype > 1 	AND categoryid >= '899' AND categoryid <> '9001'  AND categoryid <> '9999'  AND barcode not like (N'978%') and commodityname not like (N'%非%码%') AND barcode not like (N'1%') AND barcode not like (N'2%') AND status != 4 AND submittime >= '"+ar[9]+"' AND submittime <= '"+ar[10]+"' AND realname = '"+ar[18]+"' and cityname='"+ar[23]+"'")
            raw3 = feicaiji.fetchone()  # 读取所有

            # 新品采集总量
            xp_zl.execute("SELECT COUNT( DISTINCT id ) FROM w_commodity WHERE datatype = 1 AND categoryid != '9001' AND submittime >= '"+ar[9]+"' AND submittime <= '"+ar[10]+"' AND realname = '"+ar[18]+"' AND status != 4 and cityname='"+ar[23]+"'")
            raw6 = xp_zl.fetchone()  # 读取所有

            # 新品采集客户
            xp_kh.execute("SELECT COUNT( DISTINCT id ) FROM w_commodity WHERE datatype = 1 AND categoryid != '9001' AND submittime >= '"+ar[9]+"' AND submittime <= '"+ar[10]+"' AND realname = '"+ar[18]+"' AND brandtype = '2' AND status != 4 and cityname='"+ar[23]+"'")
            raw4 = xp_kh.fetchone()  # 读取所有

            # 新品采集重点
            xp_zd.execute("SELECT COUNT( DISTINCT id ) FROM w_commodity WHERE datatype = 1 AND categoryid != '9001' AND submittime >= '"+ar[9]+"' AND submittime <= '"+ar[10]+"' AND realname = '" +ar[18] + "' AND brandtype = '1'AND status != 4 and cityname='"+ar[23]+"'")
            raw5 = xp_zd.fetchone()  # 读取所有

            # 新品采集麒麟
            xp_ql.execute("SELECT COUNT( DISTINCT id ) FROM w_commodity WHERE categoryid = '9001' AND submittime >= '" + ar[9] + "' AND submittime <= '" + ar[10] + "' AND status != 4 and realname = '" + ar[18] + "' and cityname='"+ar[23]+"'")
            raw7 = xp_ql.fetchone()  # 读取所有

            # 通过率 wis总数
            fkl_wis_2.execute("SELECT COUNT( DISTINCT id ) FROM w_commodity WHERE categoryid != '9001' AND submittime >= '" + ar[9] + "' AND submittime <= '" + ar[10] + "' and datatype!='1' AND realname = '" + ar[18] + "' and cityname='"+ar[23]+"'")
            raw8_2 = fkl_wis_2.fetchone()  # 读取所有

            # 通过率_wis
            fkl_wis.execute("SELECT COUNT( DISTINCT id ) FROM w_commodity WHERE categoryid != '9001' AND submittime >= '" + ar[9] + "' AND submittime <= '" + ar[10] + "' and datatype!='1' AND STATUS != 4 AND realname = '" + ar[18] + "' and cityname='"+ar[23]+"'")
            raw8 = fkl_wis.fetchone()  # 读取所有
            if raw8[0]==0 or raw8_2[0]==0:
                tgl_wis=0
            else:
                tgl_wis=round(raw8[0]/raw8_2[0])*100

            # 通过率_常规
            fkl_cg.execute("SELECT COUNT( DISTINCT id) FROM	w_commodity WHERE submittime >= '" + ar[9] + "' AND submittime <= '" + ar[10] + "' AND status != 4 AND datatype = '1' AND categoryid != '9001' and realname='" + ar[18] + "' and cityname='"+ar[23]+"'")
            raw9 = fkl_cg.fetchone()  # 读取所有

            fkl_cg_2.execute("SELECT COUNT( DISTINCT id) FROM w_commodity WHERE submittime >= '" + ar[9] + "' AND submittime <= '" + ar[10] + "' AND datatype = '1' AND categoryid != '9001' and realname='" + ar[18] + "' and cityname='"+ar[23]+"'")
            raw9_zl = fkl_cg_2.fetchone()  # 读取所有
            if raw9[0]==0 or raw9_zl[0]==0:
                tgl_cg=0
            else:
                tgl_cg=round(raw9[0]/raw9_zl[0])*100

            # 通过率_麒麟
            fkl_ql.execute("SELECT COUNT( DISTINCT id) FROM w_commodity WHERE submittime >= '" + ar[9] + "' AND submittime <= '" + ar[10] + "' AND status != 4 AND categoryid = '9001' and realname='" + ar[18] + "' and cityname='"+ar[23]+"'")
            raw10 = fkl_ql.fetchone()  # 读取所有
            fkl_ql_zl.execute("SELECT COUNT( DISTINCT id) FROM w_commodity WHERE submittime >= '" + ar[9] + "' AND submittime <= '" + ar[10] + "' AND categoryid = '9001' and realname='" + ar[18] + "' and cityname='"+ar[23]+"'")
            raw10_zl = fkl_ql_zl.fetchone()  # 读取所有
            if raw10[0]==0 or raw10_zl[0]==0:
                tgl_ql=0
            else:
                tgl_ql=round(raw10[0]/raw10_zl[0])*100

            # 3周绩效
            # 自动评价 基础任务目标 wis—任务 renwul 绩效统计wis-任务 round(raw2[0]+raw2[0]*0.8)
            # 正常周：ar[13]  sz="是否申请三周绩效"
            pci=ar[2]+ar[3]
            xiujia.execute("SELECT * FROM sanzhoujixiao WHERE name='" + ar[18] + "'")
            if xiujia is not None:
                sz = "否"
            else:
                raw111 = xiujia.fetchall()  # 读取所有
                for arr in raw111:
                    if arr[2] == pci and arr[3] == ar[4]:
                        sz = "是"
                    else:
                        sz = "否"
            jc_wis=renwul
            jx_wis=round(raw2[0]+raw3[0]*0.8)
            if jc_wis==0 or jx_wis==0:
                jz="不达标"
                jl=0
            else:
                if ar[13] == "正常周":
                    if sz == "否":
                        if round(jx_wis / jc_wis,2) >= 1.75:
                           jz="荣耀奖"
                           if ar[4] == '1':
                               jl=110
                           elif ar[4] == '2':
                               jl=154
                           elif ar[4] == '3':
                               jl=176
                           elif ar[4] == '4':
                               jl=110
                           elif ar[4] == '5':
                               jl = 0
                        elif round(jx_wis / jc_wis,2) >= 1.45 and round(jc_wis / jx_wis,2) < 1.75:
                           jz="星光奖"
                           if ar[4] == '1':
                               jl=80
                           elif ar[4] == '2':
                               jl=112
                           elif ar[4] == '3':
                               jl=128
                           elif ar[4] == '4':
                               jl=80
                           elif ar[4] == '5':
                               jl=0
                        elif round(jx_wis / jc_wis,2) >= 1 and round(jc_wis / jx_wis,2) < 1.45:
                           jz="达标"
                           jl = 0
                        else :
                           jz="不达标"
                           jl = 0
                    else:
                        if round(jx_wis / jc_wis,2) >= 1.5:
                           jz="星光奖"
                        elif round(jx_wis / jc_wis,2) >= 0.75 and round(jc_wis / jx_wis,2) < 1.5:
                           jz="达标"
                        elif round(jx_wis / jc_wis,2) < 0.75:
                           jz="不达标"
                           jl = 0
                else:
                    if jx_wis > jc_wis:
                       jz="达标"
                       jl=0
                    else:
                       jz="不达标"
                       jl = 0

            #麒麟和常规任务不达标降档
            if ar[4] == '1':
                if (raw7[0] < 5 and raw6[0] >= 5) or (raw7[0] >= 5 and raw6[0] < 5) :
                    if jz=="荣耀奖":
                        jz="星光奖"
                        jl=80
                    elif jz=="星光奖":
                        jz="达标"
                        jl=0
                    elif jz=="达标":
                        jz="不达标"
                        jl=0
                elif raw7[0] < 5 and raw6[0] < 5 :
                    if jz == "荣耀奖":
                        jz = "达标"
                        jl = 0
                    elif jz == "星光奖":
                        jz = "不达标"
                        jl = 0
                    elif jz=="达标":
                        jz="不达标"
                        jl=0
            elif ar[4] == '2':
                if (raw7[0] < 5 and raw6[0] >= 5) or (raw7[0] >= 5 and raw6[0] < 5) :
                    if jz=="荣耀奖":
                        jz="星光奖"
                        jl=112
                    elif jz=="星光奖":
                        jz="达标"
                        jl=0
                    elif jz=="达标":
                        jz="不达标"
                        jl=0
                elif raw7[0] < 5 and raw6[0] < 5 :
                    if jz == "荣耀奖":
                        jz = "达标"
                        jl = 0
                    elif jz == "星光奖":
                        jz = "不达标"
                        jl = 0
                    elif jz=="达标":
                        jz="不达标"
                        jl=0
            elif ar[4] == '3':
                if (raw7[0] < 5 and raw6[0] >= 5) or (raw7[0] >= 5 and raw6[0] < 5):
                    if jz == "荣耀奖":
                        jz = "星光奖"
                        jl = 128
                    elif jz == "星光奖":
                        jz = "达标"
                        jl = 0
                    elif jz=="达标":
                        jz="不达标"
                        jl=0
                elif raw7[0] < 5 and raw6[0] < 5:
                    if jz == "荣耀奖":
                        jz = "达标"
                        jl = 0
                    elif jz == "星光奖":
                        jz = "不达标"
                        jl = 0
                    elif jz=="达标":
                        jz="不达标"
                        jl=0
            elif ar[4] == '4':
                if (raw7[0] < 5 and raw6[0] >= 5) or (raw7[0] >= 5 and raw6[0] < 5):
                    if jz == "荣耀奖":
                        jz = "星光奖"
                        jl = 80
                    elif jz == "星光奖":
                        jz = "达标"
                        jl = 0
                    elif jz=="达标":
                        jz="不达标"
                        jl=0
                elif raw7[0] < 5 and raw6[0] < 5:
                    if jz == "荣耀奖":
                        jz = "达标"
                        jl = 0
                    elif jz == "星光奖":
                        jz = "不达标"
                        jl = 0
                    elif jz=="达标":
                        jz="不达标"
                        jl=0
            elif ar[4] == '5':
                if (raw7[0] < 5 and raw6[0] >= 5) or (raw7[0] >= 5 and raw6[0] < 5) :
                    if jz=="荣耀奖":
                        jz="星光奖"
                        jl=0
                    elif jz=="星光奖":
                        jz="达标"
                        jl=0
                    elif jz=="达标":
                        jz="不达标"
                        jl=0
                elif raw7[0] < 5 and raw6[0] < 5 :
                    if jz == "荣耀奖":
                        jz = "达标"
                        jl = 0
                    elif jz == "星光奖":
                        jz = "不达标"
                        jl = 0
                    elif jz=="达标":
                        jz="不达标"
                        jl=0

            #占比1
            if raw4[0]==0 or raw6[0]==0:
                zb1 = 0
            else:
                zb1 = str(round(raw4[0]/raw6[0]*100))+'%'
            #占比1
            if raw5[0]==0 or raw6[0]==0:
                zb2 = 0
            else:
                zb2 = str(round(raw5[0]/raw6[0]*100))+'%'

            #mydata 任务量
            #获取当前周的 日期 monday是 本周的 星期一 sunday是本周的星期天
            monday, sunday = datetime.date.today(), datetime.date.today()
            one_day = datetime.timedelta(days=1)
            while monday.weekday() != 0:
                monday -= one_day
            while sunday.weekday() != 6:
                sunday += one_day
            mydata.execute("SELECT count(*) FROM mission_up where querentime between '"+str(monday)+"' and '"+str(sunday)+"' and querenren='" + ar[18] + "' ")
            raw_mydata = mydata.fetchone()  # 读取所有


            #ar[8]代表没周结束日
            #dqtime 本地时间的 年月 日的日
            dqtime_nian=ar[8].split('-')
            if str(dqtime_nian[2]) > '21' :
                dqtime_zhouqi = str((dqtime_nian[0]) + (dqtime_nian[1]))
                dqtime_zhouqi = int(zhouqi) + 1
            else:
                dqtime_zhouqi = (str(dqtime_nian[0]) + str(dqtime_nian[1]))

            c.append({
                        'nianfen':zhouqi,
                        'pj':ar[2],
                        'pici':ar[3],
                        'zhou':ar[4],
                        'shujuzhouqi':ar[5],
                        'kaohezhouqi':ar[6],
                        'sj_kaishiri':ar[7],
                        'sj_jiesuri':ar[8],
                        'ke_kaishiri':ar[9],
                        'ke_jiesuri':ar[10],
                        'week':ar[11],
                        'jidu':ar[12],
                        'jiexiaoleixing':ar[13],
                        'beizhu':ar[14],
                        'gongzizhouqi':ar[15],
                        'name':ar[18],
                        'quyu':ar[23],
                        'diqu':ar[22],
                        'renwuliang': renwul,
                        'jcrw_changguirenwu':'5',
                        'jcrw_qilin':'5',
                        'wiscj_caijipin':raw2[0],
                        'wiscj_feicaiji':raw3[0],
                        'wiscj_zongliang':raw2[0]+raw3[0],
                        'xpcj_zongliang':raw6[0],
                        'xpcj_kehu':raw4[0],
                        'xpcj_zhongdian':raw5[0],
                        'xpcj_zhanbi':zb1,
                        'xpcj_zhanbi2':zb2,
                        'qlcjl_hegeshuliang':raw7[0],
                        'fkl_wis':str(tgl_wis)+'%',
                        'fkl_changgui':str(tgl_cg)+'%',
                        'fkl_qilin':str(tgl_ql)+'%',
                        'jxtj_wisrenwu':round(raw2[0]+raw3[0]*0.8),
                        'jxtj_changguirenwu':raw6[0],
                        'jxtj_qilin':raw7[0],
                        'sfxj_shifouxiujia':sz,
                        'zdpj_pingjia':jz,
                        'mydata_mydataqueren':raw_mydata,
                        'zdpj_jiangli':jl,
                        'lwjs_zhouqi': dqtime_zhouqi
                     })
            tst=jx_jixiao(
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
                wiscj_caijipin=raw2[0],
                wiscj_feicaiji=raw3[0],
                wiscj_zongliang=raw2[0]+raw3[0],
                xpcj_zongliang=raw6[0],
                xpcj_kehu=raw4[0],
                xpcj_zhongdian=raw5[0],
                xpcj_zhanbi=zb1,
                xpcj_zhanbi2=zb2,
                qlcjl_hegeshuliang=raw7[0],
                fkl_wis=str(tgl_wis)+'%',
                fkl_changgui=str(tgl_cg)+'%',
                fkl_qilin=str(tgl_ql)+'%',
                jxtj_wisrenwu=round(raw2[0]+raw3[0]*0.8),
                jxtj_changguirenwu=raw6[0],
                jxtj_qilin=raw7[0],
                sfxj_shifouxiujia=sz,
                zdpj_pingjia=jz,
                mydata=raw_mydata,
                zdpj_jiangli=jl,
                lwjs_zhouqi=dqtime_zhouqi).save()



    data['list'] = (list(c))
    return JsonResponse(data, safe=False)
#后台跑库
def houtai_jx2(request):
    jx_jixiao.objects.all().delete()

    data = {}
    c=[]
    renwul=''
    zb1=''
    pci =''
    sz=''
    zl=''
    tgl_wis=''

    if request.GET.get('pici'):
        pici = request.GET.get('pici')
        week = request.GET.get('week')
    else:
        pici = '1'
        week = '2'
    cursor1 = connection.cursor()
    caiji = connection.cursor()
    feicaiji=connection.cursor()
    xp_zl=connection.cursor()
    xp_kh=connection.cursor()
    xp_zd=connection.cursor()
    xp_ql=connection.cursor()
    fkl_wis=connection.cursor()
    fkl_wis_2=connection.cursor()
    fkl_cg=connection.cursor()
    fkl_cg_2=connection.cursor()
    fkl_ql=connection.cursor()
    xiujia=connection.cursor()
    fkl_ql_zl=connection.cursor()
    mydata=connection.cursor()



    #基础表
    cursor1.execute("SELECT * FROM `jx_zhouqibiao`,`user`,`jx_zhourenwu` WHERE USER.qx = '4' AND jx_zhourenwu.user_id=user.id")
    raw =cursor1.fetchall()  # 读取所有
    dqdate = datetime.datetime.now().strftime('%Y-%m-%d')
    print(dqdate)
    for ar in raw:
        if dqdate <= ar[9] :
           break
        else :
            #周期2020P1-1
            zhouqi = str(ar[1])+str(ar[2])+str(ar[3])+"-"+str(ar[4])
            #ar[4] 批次是周
            if ar[4]=='1':
                renwul=round(int(ar[28])*0.2)
            elif ar[4]=='2':
                renwul=round(int(ar[28])*0.28)
            elif ar[4]=='3':
                renwul=round(int(ar[28])*0.32)
            elif ar[4]=='4':
                renwul=round(int(ar[28])*0.2)
            elif ar[4]=='5':
                renwul=round(int(ar[28])*0.24)


            # wis采集
            caiji.execute("SELECT COUNT( DISTINCT id) FROM  jx_lurutongji WHERE chaolushijian >= '"+ar[9]+"' AND chaolushijian <= '"+ar[10]+"' AND shujuleixing != 1 AND pinleidaima != '9001' and pinleidaima < '899' AND realname = '"+ar[18]+"' and xingming = '"+ar[23]+"' AND status != 4;")
            raw2 = caiji.fetchone()  # 读取所有

            # wis非采集
            feicaiji.execute("SELECT COUNT( DISTINCT id ) FROM w_commodity WHERE shujuleixing > 1 	AND pinleidaima >= '899' AND pinleidaima <> '9001'  AND pinleidaima <> '9999'  AND tiaoma not like (N'978%') and shangpinquancheng not like (N'%非%码%') AND tiaoma not like (N'1%') AND tiaoma not like (N'2%') AND status != 4 AND chaolushijian >= '"+ar[9]+"' AND chaolushijian <= '"+ar[10]+"' AND xingming = '"+ar[18]+"' and difangzhan='"+ar[23]+"'")
            raw3 = feicaiji.fetchone()  # 读取所有

            # 新品采集总量
            xp_zl.execute("SELECT COUNT( DISTINCT id ) FROM w_commodity WHERE datatype = 1 AND categoryid != '9001' AND submittime >= '"+ar[9]+"' AND submittime <= '"+ar[10]+"' AND realname = '"+ar[18]+"' AND status != 4 and cityname='"+ar[23]+"'")
            raw6 = xp_zl.fetchone()  # 读取所有

            # 新品采集客户
            xp_kh.execute("SELECT COUNT( DISTINCT id ) FROM w_commodity WHERE datatype = 1 AND categoryid != '9001' AND submittime >= '"+ar[9]+"' AND submittime <= '"+ar[10]+"' AND realname = '"+ar[18]+"' AND brandtype = '2' AND status != 4 and cityname='"+ar[23]+"'")
            raw4 = xp_kh.fetchone()  # 读取所有

            # 新品采集重点
            xp_zd.execute("SELECT COUNT( DISTINCT id ) FROM w_commodity WHERE datatype = 1 AND categoryid != '9001' AND submittime >= '"+ar[9]+"' AND submittime <= '"+ar[10]+"' AND realname = '" +ar[18] + "' AND brandtype = '1'AND status != 4 and cityname='"+ar[23]+"'")
            raw5 = xp_zd.fetchone()  # 读取所有

            # 新品采集麒麟
            xp_ql.execute("SELECT COUNT( DISTINCT id ) FROM w_commodity WHERE categoryid = '9001' AND submittime >= '" + ar[9] + "' AND submittime <= '" + ar[10] + "' AND status != 4 and realname = '" + ar[18] + "' and cityname='"+ar[23]+"'")
            raw7 = xp_ql.fetchone()  # 读取所有

            # 通过率 wis总数
            fkl_wis_2.execute("SELECT COUNT( DISTINCT id ) FROM w_commodity WHERE categoryid != '9001' AND submittime >= '" + ar[9] + "' AND submittime <= '" + ar[10] + "' and datatype!='1' AND realname = '" + ar[18] + "' and cityname='"+ar[23]+"'")
            raw8_2 = fkl_wis_2.fetchone()  # 读取所有

            # 通过率_wis
            fkl_wis.execute("SELECT COUNT( DISTINCT id ) FROM w_commodity WHERE categoryid != '9001' AND submittime >= '" + ar[9] + "' AND submittime <= '" + ar[10] + "' and datatype!='1' AND STATUS != 4 AND realname = '" + ar[18] + "' and cityname='"+ar[23]+"'")
            raw8 = fkl_wis.fetchone()  # 读取所有
            if raw8[0]==0 or raw8_2[0]==0:
                tgl_wis=0
            else:
                tgl_wis=round(raw8[0]/raw8_2[0])*100

            # 通过率_常规
            fkl_cg.execute("SELECT COUNT( DISTINCT id) FROM	w_commodity WHERE submittime >= '" + ar[9] + "' AND submittime <= '" + ar[10] + "' AND status != 4 AND datatype = '1' AND categoryid != '9001' and realname='" + ar[18] + "' and cityname='"+ar[23]+"'")
            raw9 = fkl_cg.fetchone()  # 读取所有

            fkl_cg_2.execute("SELECT COUNT( DISTINCT id) FROM w_commodity WHERE submittime >= '" + ar[9] + "' AND submittime <= '" + ar[10] + "' AND datatype = '1' AND categoryid != '9001' and realname='" + ar[18] + "' and cityname='"+ar[23]+"'")
            raw9_zl = fkl_cg_2.fetchone()  # 读取所有
            if raw9[0]==0 or raw9_zl[0]==0:
                tgl_cg=0
            else:
                tgl_cg=round(raw9[0]/raw9_zl[0])*100

            # 通过率_麒麟
            fkl_ql.execute("SELECT COUNT( DISTINCT id) FROM w_commodity WHERE submittime >= '" + ar[9] + "' AND submittime <= '" + ar[10] + "' AND status != 4 AND categoryid = '9001' and realname='" + ar[18] + "' and cityname='"+ar[23]+"'")
            raw10 = fkl_ql.fetchone()  # 读取所有
            fkl_ql_zl.execute("SELECT COUNT( DISTINCT id) FROM w_commodity WHERE submittime >= '" + ar[9] + "' AND submittime <= '" + ar[10] + "' AND categoryid = '9001' and realname='" + ar[18] + "' and cityname='"+ar[23]+"'")
            raw10_zl = fkl_ql_zl.fetchone()  # 读取所有
            if raw10[0]==0 or raw10_zl[0]==0:
                tgl_ql=0
            else:
                tgl_ql=round(raw10[0]/raw10_zl[0])*100

            # 3周绩效
            pci=ar[2]+ar[3]
            xiujia.execute("SELECT * FROM sanzhoujixiao WHERE name='" + ar[18] + "'")
            if xiujia is not None:
                sz = "否"
            else:
                raw111 = xiujia.fetchall()  # 读取所有
                for arr in raw111:
                    if arr[2] == pci and arr[3] == ar[4]:
                        sz = "是"
                    else:
                        sz = "否"

            #自动评价 基础任务目标 wis—任务 renwul 绩效统计wis-任务 round(raw2[0]+raw2[0]*0.8)
            #正常周：ar[13]  sz="是否申请三周绩效"
            jc_wis=renwul
            jx_wis=round(raw2[0]+raw3[0]*0.8)

            if jc_wis==0 or jx_wis==0:
                jz="不达标"
            else:
                if ar[13] == "正常周":
                    if sz == "否":
                        if round(jx_wis / jc_wis) >= 1.75:
                           jz="荣耀奖"
                        elif round(jx_wis / jc_wis) >= 1.45 and round(jc_wis / jx_wis) < 1.75:
                           jz="星光奖"
                        elif round(jx_wis / jc_wis) >= 1 and round(jc_wis / jx_wis) < 1.45:
                           jz="达标"
                        else :
                           jz="不达标"
                    else:
                        if round(jx_wis / jc_wis) >= 1.5:
                           jz="星光奖"
                        elif round(jx_wis / jc_wis) >= 0.75 and round(jc_wis / jx_wis) < 1.5:
                           jz="达标"
                        elif round(jx_wis / jc_wis) < 0.75:
                           jz="不达标"
                else:
                    if jx_wis > jc_wis:
                       jz="达标"
                    else:
                       jz="不达标"
            #占比1
            if raw4[0]==0 or raw6[0]==0:
                zb1 = 0
            else:
                zb1 = str(round(raw4[0]/raw6[0]*100))+'%'
            #占比1
            if raw5[0]==0 or raw6[0]==0:
                zb2 = 0
            else:
                zb2 = str(round(raw5[0]/raw6[0]*100))+'%'

            #mydata 任务量
            #获取当前周的 日期 monday是 本周的 星期一 sunday是本周的星期天
            monday, sunday = datetime.date.today(), datetime.date.today()
            one_day = datetime.timedelta(days=1)
            while monday.weekday() != 0:
                monday -= one_day
            while sunday.weekday() != 6:
                sunday += one_day
            mydata.execute("SELECT count(*) FROM mission_up where querentime between '"+str(monday)+"' and '"+str(sunday)+"' and querenren='" + ar[18] + "' ")
            raw_mydata = mydata.fetchone()  # 读取所有




            c.append({
                        'nianfen':zhouqi,
                        'pj':ar[2],
                        'pici':ar[3],
                        'zhou':ar[4],
                        'shujuzhouqi':ar[5],
                        'kaohezhouqi':ar[6],
                        'sj_kaishiri':ar[7],
                        'sj_jiesuri':ar[8],
                        'ke_kaishiri':ar[9],
                        'ke_jiesuri':ar[10],
                        'week':ar[11],
                        'jidu':ar[12],
                        'jiexiaoleixing':ar[13],
                        'beizhu':ar[14],
                        'gongzizhouqi':ar[15],
                        'name':ar[18],
                        'quyu':ar[23],
                        'diqu':ar[22],
                        'renwuliang': renwul,
                        'jcrw_changguirenwu':'5',
                        'jcrw_qilin':'5',
                        'wiscj_caijipin':raw2[0],
                        'wiscj_feicaiji':raw3[0],
                        'wiscj_zongliang':raw2[0]+raw3[0],
                        'xpcj_zongliang':raw6[0],
                        'xpcj_kehu':raw4[0],
                        'xpcj_zhongdian':raw5[0],
                        'xpcj_zhanbi':zb1,
                        'xpcj_zhanbi2':zb2,
                        'qlcjl_hegeshuliang':raw7[0],
                        'fkl_wis':str(tgl_wis)+'%',
                        'fkl_changgui':str(tgl_cg)+'%',
                        'fkl_qilin':str(tgl_ql)+'%',
                        'jxtj_wisrenwu':round(raw2[0]+raw3[0]*0.8),
                        'jxtj_changguirenwu':raw6[0],
                        'jxtj_qilin':raw7[0],
                        'sfxj_shifouxiujia':sz,
                        'zdpj_pingjia':jz,
                        'mydata_mydataqueren':raw_mydata
                     })
            tst=jx_jixiao(
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
                wiscj_caijipin=raw2[0],
                wiscj_feicaiji=raw3[0],
                wiscj_zongliang=raw2[0]+raw3[0],
                xpcj_zongliang=raw6[0],
                xpcj_kehu=raw4[0],
                xpcj_zhongdian=raw5[0],
                xpcj_zhanbi=zb1,
                xpcj_zhanbi2=zb2,
                qlcjl_hegeshuliang=raw7[0],
                fkl_wis=str(tgl_wis)+'%',
                fkl_changgui=str(tgl_cg)+'%',
                fkl_qilin=str(tgl_ql)+'%',
                jxtj_wisrenwu=round(raw2[0]+raw3[0]*0.8),
                jxtj_changguirenwu=raw6[0],
                jxtj_qilin=raw7[0],
                sfxj_shifouxiujia=sz,
                zdpj_pingjia=jz,
                mydata=raw_mydata,
                zdpj_jiangli=jz,
                ).save()


    data['list'] = (list(c))
    return JsonResponse(data, safe=False)

#绩效表
def jixiao(request):
    data = {}
    if request.GET.get('pici'):
        pici = request.GET.get('pici')
        week = request.GET.get('week')
        book = jx_jixiao.objects.filter(pici=pici,zhou=week).all().values()  # 获取值values放后面
    else:
        book = jx_jixiao.objects.all().values()  # 获取值values放后面
    data['list'] = (list(book))
    return JsonResponse(data)

#每周数据采集情况 表1
def tongjitubiao(request):
    data = {}
    c = []
    cursor1 = connection.cursor()
    # 基础表
    cursor1.execute("SELECT caijipinshuliang,feicaishuliang,zhongxinchuli,changguitijiaoshuliang,zhouqi FROM `w_work_info_tmp` order by zhouqi desc limit 0,14")
    raw = cursor1.fetchall()  # 读取所有
    for ar in raw:
        c.append({
            'caijipinshuliang': str(ar[0]),
            'feicaishuliang': str(ar[1]),
            'zhongxinchuli': str(ar[2]),
            'changguitijiaoshuliang': str(ar[3]),
            'zhouqi':str(ar[4]),
        })
    data['list'] = (list(c))
    return JsonResponse(data)

#提交量-P表 表2
def tijiaoliangP(request):
    data = {}
    c = []
    cursor1 = connection.cursor()
    # 基础表
    cursor1.execute("SELECT * FROM (SELECT pci,newcount,wis,intercept,collect,uncollect,qilin FROM `w_monitor` order by pci desc ) aa ORDER BY pci")
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

#常规数据抄录情况连续监测 表7
def changgui(request):
    data = {}
    all = []
    c=[]
    newcount = []
    f=connection.cursor()
    cursor1 = connection.cursor()
    cursor2 = connection.cursor()
    # 基础表
    i=0;

    f.execute("SELECT count(*) FROM `w_monitor` order by year asc")
    rawcount = f.fetchall()
    cursor1.execute("SELECT DISTINCT(year) FROM `w_monitor` order by year asc")
    raw = cursor1.fetchall()  # 读取所有
    # for ar in raw:
    #     newcount.append(dict(year=ar[i])),
    #     cursor2.execute("SELECT *  FROM `w_monitor` where year='"+ar[i]+"' order by id asc")
    #     raw2 = cursor2.fetchall()  # 读取所有
    #     for ar2 in raw2:
    #         c[i].append(ar2[4])
    #         print(c)
    #     newcount.append({'newcount':c[i]})

    data['list'] = (list(newcount))
    return JsonResponse(data)

#新图表 表8
def xintubiao(request):
    data = {}
    c = []
    newcount = []
    cursor2 = connection.cursor()
    cursor2.execute("SELECT riqi,weipipeitiaomaliang,tijiaoliang,pinci,pipeilv  FROM `w_unmatch_commit` order by riqi asc")
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

#地方图表
def difangtubiao(request):
    data = {}
    c=[]
    zrenwuliang=0
    cursor1 = connection.cursor()
    cursor1.execute("SELECT shujuzhouqi,diqu,GROUP_CONCAT(DISTINCT(name)) as name,sum(renwuliang) as renwuliang,sum(wiscj_caijipin) as wiscj_caijipin,sum(wiscj_feicaiji) as wiscj_feicaiji,sum(jcrw_changguirenwu) as jcrw_changguirenwu,sum(xpcj_zongliang) as xpcj_zongliang,sum(jcrw_qilin) as jcrw_qilin,sum(qlcjl_hegeshuliang) as qlcjl_hegeshuliang  from  `jx_jixiao`  group by name order by diqu asc;")
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

#测试图表 2个 下拉框方法
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
    c=[]
    if request.GET.get('zhouqi'):
        zhouqi =request.GET.get('zhouqi')
        cursor1 = connection.cursor()
        cursor1.execute("SELECT shujuzhouqi,diqu,GROUP_CONCAT(DISTINCT(name)) as name,sum(renwuliang) as renwuliang,sum(wiscj_caijipin) as wiscj_caijipin,sum(wiscj_feicaiji) as wiscj_feicaiji,sum(jcrw_changguirenwu) as jcrw_changguirenwu,sum(xpcj_zongliang) as xpcj_zongliang,sum(jcrw_qilin) as jcrw_qilin,sum(qlcjl_hegeshuliang) as qlcjl_hegeshuliang  from  `jx_jixiao` where shujuzhouqi='" + str(
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

#周期表后台数据
def zhouqibiao(request):
    data = {}
    c=[]
    cursor1 = connection.cursor()
    cursor1.execute("SELECT * FROM `jx_zhouqibiao`")
    raw = cursor1.fetchall()  # 读取所有
    for ar in raw:
        c.append({
            'nianfen': str(ar[1]),
            'pj': str(ar[2]),
            'pici':ar[3] ,
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

#查询方法
def find(request):
    data = {}
    if request.GET.get('find'):
        find = request.GET.get('find')
        book = jx_jixiao.objects.filter(Q(name__icontains=find)|Q(quyu__icontains=find)|Q(diqu__icontains=find)).all().values()  # 获取值values放后面
    data['list'] = (list(book))
    return JsonResponse(data)

#匹配率表

def pipeilvbiao(request):
    data = {}
    c = []
    cursor1 = connection.cursor()
    cursor1.execute("SELECT pci,hhp_matching,btp_matching,bbp_matching FROM `w_work_matching`")
    raw = cursor1.fetchall()  # 读取所有
    for ar in raw:
        c.append({
            'pci': str(ar[0]),
            'hhp_matching': str(ar[1]),
            'btp_matching': str(ar[2]),
            'bbp_matching':str(ar[3]),
        })
    data['list'] = (list(c))
    return JsonResponse(data)

def test(request):
    tup1 = ('physics', 'chemistry', 1997, 2000);
    tup2 = (1, 2, 3, 4, 5, 6, 7);

    print("tup1[0]: ", tup1[0])
    print("tup2[1:5]: ", tup2[1:5])
    return HttpResponse()