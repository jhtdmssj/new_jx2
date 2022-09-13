import json
from houtai.fw3.MongoDBHelper import MongoDBHelper
from django.contrib.sites import requests
from django.http import JsonResponse,HttpResponse



def api_code(request):
    data = {}
    c = []
    a=str(request.GET.get('code'))
    db = MongoDBHelper(db='produce_db')
    results = db.select_all_collection('api_template', {'tiaoma': a})

    for result in (results):
        c.append({
            'tiaoma': result['tiaoma'],
            'fenlei': result['fenlei'],
            'quancheng': result['quancheng'],
            'jiage': result['jiage'],
            'qudao': result['qudao'],
            'wangzhi': result['wangzhi'],
            'tupian': result['tupian'],
            'dianpu': result['dianpu'],
            'caijiriqi': result['caijiriqi']
        })

    return HttpResponse(json.dumps(c,ensure_ascii=False),content_type='application/json;charset=utf-8')

if __name__ == '__main__':
   api_code()


