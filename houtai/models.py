# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class w_work_info_tmp(models.Model):
    daochushijian = models.CharField(max_length=500)
    tijiaoshijian = models.CharField(max_length=500)
    jiezhishijian = models.CharField(max_length=500)
    pci = models.CharField(max_length=500)
    zhouqi = models.CharField(max_length=500)
    daochuzongliang = models.CharField(max_length=500)
    wisfankui = models.CharField(max_length=500)
    changguifankui = models.CharField(max_length=500)
    qilinfankui = models.CharField(max_length=500)
    zhongxinchulifankui = models.CharField(max_length=500)
    fankuizongshuliang = models.CharField(max_length=500)
    chenggongtijiaozongshuliang = models.CharField(max_length=500)
    yousaomiaojilutiaoshu = models.CharField(max_length=500)
    yousaomiaojilupinci = models.CharField(max_length=500)
    wistijiaoshuliang = models.CharField(max_length=500)
    youdangpsaomiaoshuliangwis = models.CharField(max_length=500)
    dangpzhanbi = models.CharField(max_length=500)
    wisdangpsaomiaopinci = models.CharField(max_length=500)
    caijipinshuliang = models.CharField(max_length=500)
    caijipinzhaopianshuliang = models.CharField(max_length=500)
    caizhaopianbi = models.CharField(max_length=500)
    feicaishuliang = models.CharField(max_length=500)
    feicaizhaopianshuliang = models.CharField(max_length=500)
    feicaizhaopianbi = models.CharField(max_length=500)
    wiszhaopianzhanbi = models.CharField(max_length=500)
    caijipinbili = models.CharField(max_length=500)
    feicaijibili = models.CharField(max_length=500)
    changguitijiaoshuliang = models.CharField(max_length=500)
    youdangpsaomiaoshuliangchanggui = models.CharField(max_length=500)
    changguidangpsaomiaopinci = models.CharField(max_length=500)
    kehupinpaishuliang = models.CharField(max_length=500)
    kehupinpaiyousaomiaoshuliang = models.CharField(max_length=500)
    kehupinpaibeisaomiaopinci = models.CharField(max_length=500)
    zhongdianpinpaishuliang = models.CharField(max_length=500)
    zhongdianpinpaiyousaomiaoshuliang = models.CharField(max_length=500)
    zhongdianpinpaibeisaomiaopinci = models.CharField(max_length=500)
    changguizhaopianshuliang = models.CharField(max_length=500)
    zhaopianzhanbi = models.CharField(max_length=500)
    zhongxinchuli = models.CharField(max_length=500)
    yousaomiaojilushuliang = models.CharField(max_length=500)
    beisaomiaopinci = models.CharField(max_length=500)
    jingdongbianma = models.CharField(max_length=500)
    qilin9001 = models.CharField(max_length=500)
    changguifei69shangpincaijishuliang = models.CharField(max_length=500)
    wisfei69shangpincaijishuliang = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'w_work_info_tmp'


class jx_jixiao(models.Model):
    nianfen = models.CharField(max_length=500)
    pj = models.CharField(max_length=500)
    pici = models.CharField(max_length=500)
    zhou = models.CharField(max_length=500)
    shujuzhouqi = models.CharField(max_length=500)
    kaohezhouqi = models.CharField(max_length=500)
    sj_kaishiri = models.CharField(max_length=500)
    sj_jiesuri = models.CharField(max_length=500)
    ke_kaishiri = models.CharField(max_length=500)
    ke_jiesuri = models.CharField(max_length=500)
    week = models.CharField(max_length=500)
    jidu = models.CharField(max_length=500)
    jiexiaoleixing = models.CharField(max_length=500)
    beizhu = models.CharField(max_length=500)
    gongzizhouqi = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    quyu = models.CharField(max_length=500)
    diqu = models.CharField(max_length=500)
    renwuliang = models.CharField(max_length=500)
    jcrw_changguirenwu = models.CharField(max_length=500)
    jcrw_qilin = models.CharField(max_length=500)
    wiscj_caijipin = models.CharField(max_length=500)
    wiscj_feicaiji = models.CharField(max_length=500)
    wiscj_zongliang = models.CharField(max_length=500)
    xpcj_zongliang = models.CharField(max_length=500)
    xpcj_kehu = models.CharField(max_length=500)
    xpcj_zhongdian = models.CharField(max_length=500)
    xpcj_zhanbi = models.CharField(max_length=500)
    xpcj_zhanbi2 = models.CharField(max_length=500)
    qlcjl_hegeshuliang = models.CharField(max_length=500)
    fkl_wis = models.CharField(max_length=500)
    fkl_changgui = models.CharField(max_length=500)
    fkl_qilin = models.CharField(max_length=500)
    jxtj_wisrenwu = models.CharField(max_length=500)
    jxtj_changguirenwu = models.CharField(max_length=500)
    jxtj_qilin = models.CharField(max_length=500)
    sfxj_shifouxiujia = models.CharField(max_length=500)
    zdpj_pingjia = models.CharField(max_length=500)
    mydata = models.CharField(max_length=500)
    zdpj_jiangli = models.CharField(max_length=500)
    lwjs_zhouqi=models.CharField(max_length=500)
    sjqr_tiaozheng=models.CharField(max_length=500)
    class Meta:
        managed = False
        db_table = 'jx_jixiao'


class jx_jixiao_all(models.Model):
    nianfen = models.CharField(max_length=500)
    pj = models.CharField(max_length=500)
    pici = models.CharField(max_length=500)
    zhou = models.CharField(max_length=500)
    shujuzhouqi = models.CharField(max_length=500)
    kaohezhouqi = models.CharField(max_length=500)
    sj_kaishiri = models.CharField(max_length=500)
    sj_jiesuri = models.CharField(max_length=500)
    ke_kaishiri = models.CharField(max_length=500)
    ke_jiesuri = models.CharField(max_length=500)
    week = models.CharField(max_length=500)
    jidu = models.CharField(max_length=500)
    jiexiaoleixing = models.CharField(max_length=500)
    beizhu = models.CharField(max_length=500)
    gongzizhouqi = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    quyu = models.CharField(max_length=500)
    diqu = models.CharField(max_length=500)
    renwuliang = models.CharField(max_length=500)
    jcrw_changguirenwu = models.CharField(max_length=500)
    jcrw_qilin = models.CharField(max_length=500)
    wiscj_caijipin = models.CharField(max_length=500)
    wiscj_feicaiji = models.CharField(max_length=500)
    wiscj_zongliang = models.CharField(max_length=500)
    xpcj_zongliang = models.CharField(max_length=500)
    xpcj_kehu = models.CharField(max_length=500)
    xpcj_zhongdian = models.CharField(max_length=500)
    xpcj_zhanbi = models.CharField(max_length=500)
    xpcj_zhanbi2 = models.CharField(max_length=500)
    qlcjl_hegeshuliang = models.CharField(max_length=500)
    fkl_wis = models.CharField(max_length=500)
    fkl_changgui = models.CharField(max_length=500)
    fkl_qilin = models.CharField(max_length=500)
    jxtj_wisrenwu = models.CharField(max_length=500)
    jxtj_changguirenwu = models.CharField(max_length=500)
    jxtj_qilin = models.CharField(max_length=500)
    sfxj_shifouxiujia = models.CharField(max_length=500)
    zdpj_pingjia = models.CharField(max_length=500)
    mydata = models.CharField(max_length=500)
    zdpj_jiangli = models.CharField(max_length=500)
    lwjs_zhouqi=models.CharField(max_length=500)
    sjqr_tiaozheng=models.CharField(max_length=500)
    class Meta:
        managed = False
        db_table = 'jx_jixiao_all'


class User(models.Model):
    name = models.CharField(max_length=500)
    password = models.CharField(max_length=500)
    qx = models.CharField(max_length=500)
    fjz = models.CharField(max_length=50)
    quyu = models.CharField(max_length=500)
    diqu = models.CharField(max_length=50)
    lingyun = models.CharField(max_length=50)
    tel = models.CharField(max_length=50)
    class Meta:
        managed = False
        db_table = 'user'

class JxZhouqibiao(models.Model):
        nianfen = models.CharField(max_length=255, blank=True, null=True)
        pj = models.CharField(max_length=255, blank=True, null=True)
        pici = models.CharField(max_length=255, blank=True, null=True)
        zhou = models.CharField(max_length=255, blank=True, null=True)
        shujuzhouqi = models.CharField(max_length=255, blank=True, null=True)
        kaohezhouqi = models.CharField(max_length=255, blank=True, null=True)
        sj_kaishiri = models.CharField(max_length=255, blank=True, null=True)
        sj_jiesuri = models.CharField(max_length=255, blank=True, null=True)
        ke_kaishiri = models.CharField(max_length=255, blank=True, null=True)
        ke_jiesuri = models.CharField(max_length=255, blank=True, null=True)
        week = models.CharField(max_length=255, blank=True, null=True)
        jidu = models.CharField(max_length=255, blank=True, null=True)
        jiexiaoleixing = models.CharField(max_length=50, blank=True, null=True)
        beizhu = models.CharField(max_length=50, blank=True, null=True)
        gongzizhouqi = models.CharField(max_length=255, blank=True, null=True)
        name= models.CharField(max_length=255, blank=True, null=True)
        class Meta:
            managed = False
            db_table = 'jx_zhouqibiao'


class j_mission_up(models.Model):
        tiaoma= models.CharField(max_length=255, blank=True, null=True)
        miaoshu= models.CharField(max_length=255, blank=True, null=True)
        querenshuoming= models.CharField(max_length=255, blank=True, null=True)
        beizhu= models.CharField(max_length=255, blank=True, null=True)
        renwumingcheng= models.CharField(max_length=255, blank=True, null=True)
        zhuangtai= models.CharField(max_length=255, blank=True, null=True)
        querenren= models.CharField(max_length=255, blank=True, null=True)
        imgurl= models.CharField(max_length=255, blank=True, null=True)
        querentime= models.CharField(max_length=255, blank=True, null=True)
        houimage= models.CharField(max_length=255, blank=True, null=True)
        class Meta:
            managed = False
            db_table = 'j_mission_up'
