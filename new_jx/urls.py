"""new_jx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.contrib import admin
from django.urls import path
from django.urls import re_path as url
from houtai import index,views,upload_excel,tests,jx_new_jixiao,ceshi,map,api,DX,apps

from django.conf.urls.static import static
from . import settings

urlpatterns = [
    url(r'^hello$', views.hello),
    path('login/', index.login),
    path('houtai_jx/', index.houtai_jx),
    path('zhouqibiao/', index.zhouqibiao),
    path('tongjitubiao/', index.tongjitubiao),
    path('tijiaoliangP/', index.tijiaoliangP),
    path('tijiaoliangP2/', index.tijiaoliangP2),
    path('tubiao_cons12/', index.tubiao_cons12),
    path('tubiao_cons12_xialakuang/', index.tubiao_cons12_xialakuang),
    path('nianhui_03/', index.nianhui_03),
    path('changgui/', index.changgui),
    path('changgui4/', index.changgui4),
    path('xintubiao/', index.xintubiao),
    path('sjqr_tiaozheng/', index.sjqr_tiaozheng),
    path('excel_daochu/', index.excel_daochu),
    path('excel_daochu2/', index.excel_daochu2),
    path('excel_map_daochu/', index.excel_map_daochu),
    path('mission_find/', index.mission_find),
    path('geren_mission/', index.geren_mission),
    path('tubiao_cons13/', index.tubiao_cons13),

    path('difangtubiao/', index.difangtubiao),
    path('difangtubiao_select2/', index.difangtubiao_select2),
    path('pipeilvbiao/', index.pipeilvbiao),
    path('writeFile/', index.writeFile),
    path('uploadfile/', index.uploadfile),
    path('j_mission_list/', index.j_mission_list),
    path('mission_zhuangtai/', index.mission_zhuangtai),
    path('api_code/', api.api_code),

    path('test/', index.test),
    path('jixiao/', index.jixiao),
    path('find/', index.find),
    path('timec/', index.timec),
    path('upload_excel/', upload_excel.excel),
    path('nianduxinpincaiji/', index.nianduxinpincaiji),
    path('quyufeicaizhanbi/', index.quyufeicaizhanbi),
    path('meirizidongchulishuju/', index.meirizidongchulishuju),
    path('stfchulibiao/', index.stfchulibiao),
    path('pinleicaijipaiming/', index.pinleicaijipaiming),
    path('pinleicaijipaiming_P10/', index.pinleicaijipaiming_P10),

    path('kuaidiwuliu/', tests.kuaidiwuliu),
    path('performance/', jx_new_jixiao.performance),
    path('performance2020/', jx_new_jixiao.performance2020),
    path('defen/', index.defen),
    path('defen_pci/', index.defen_pci),
    path('kaoqin/', index.kaoqin),
    path('kaoqin_ck/', index.kaoqin_ck),
    path('kaoqin_up/', index.kaoqin_up),
    path('kaoqin_del/', index.kaoqin_del),
    path('kaoqin_ck_riqi/', index.kaoqin_ck_riqi),
    path('testcs/', ceshi.testcs),
    path('map_zb/', map.map_zb),
    path('map_list/', map.map_list),
    path('map_list2/', map.map_list2),
    path('map_list_del/', map.map_list_del),
    path('map_zuobiao_list/', map.map_zuobiao_list),
    path('test_kd/', tests.test_kd),
    path('map_list_del2/', map.map_list_del2),
    path('w_stf_categoryid_count/', index.w_stf_categoryid_count),
    path('left_add/', index.left_add),
    path('left_img_add/', index.left_img_add),
    path('left_add_ck/', index.left_add_ck),
    path('left_add_ck_nr/', index.left_add_ck_nr),
    path('left_del/', index.left_del),
    path('kaoqin_ck2/', index.kaoqin_ck2),
    path('tongzhi/', index.tongzhi),
    path('tongzhi_ck/', index.tongzhi_ck),
    path('jiadian/', index.jiadian),
    path('jiadian_tj/', index.jiadian_tj),
    path('jiadian_xg/', index.jiadian_xg),
    path('jiadian_del/', index.jiadian_del),
    path('jiadian_find/', index.jiadian_find),
    path('GS1/', index.GS1),
    path('sanzhoujixiao/',index.sanzhoujixiao),
    path('sanzhoujixiao_add',index.sanzhoujixiao_add),
    path('sanzhoujixiao_find',index.sanzhoujixiao_find),
    path('zhidao_dl_add/',index.zhidao_dl_add),
    path('zhidao_xl_add/',index.zhidao_xl_add),
    path('zhidao_del/',index.zhidao_del),
    path('zhidao_dl',index.zhidao_dl),
    path('zhidao_nr/',index.zhidao_nr),
    path('zhidao_ty/',index.zhidao_ty),
    path('zhidao_up/',index.zhidao_up),
    path('dicc_img_add/',index.dicc_img_add),
    path('jiadian_daochu/',index.jiadian_daochu),

    path('qianyi/', index.qianyi),
    path('qianyi_find/', index.qianyi_find),
    path('qianyi_show/', index.qianyi_show),
    path('qianyi_zt/', index.qianyi_zt),
    path('qianyi_user/', index.qianyi_user),
    path('qianyi_upload/', index.qianyi_upload),
    path('qianyi_begin/', index.qianyi_begin),

    path('j_shujufenjie/', index.j_shujufenjie),
    path('sj_upload/', index.sj_upload),
    path('sj_add/', index.sj_add),
    path('sj_del/', index.sj_del),
    path('j_cj/', index.j_cj),
    path('cs_upload/', index.cs_upload),
    path('cs_del/', index.cs_del),

    path('kaohe_add/', index.kaohe_add),
    path('kaohe_ck/', index.kaohe_ck),
    path('kaohe_ck2/', index.kaohe_ck2),
    path('kaohe_xg/', index.kaohe_xg),
    path('kaohe_del/', index.kaohe_del),
    path('kaohe_jg/', index.kaohe_jg),
    path('kaohe_tg/', index.kaohe_tg),

    path('peixun_ck/', index.peixun_ck),
    path('peixun_xg/', index.peixun_xg),
    path('peixun_del/', index.peixun_del),

    path('DX_upload/', DX.DX_upload),
    path('process_data/', apps.process_data),
    path('show_progress/', apps.show_progress),

]

urlpatterns += static('/upload/', document_root=settings.MEDIA_ROOT)
