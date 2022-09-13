from datetime import time

from django.shortcuts import render


def hello(request):
    context = {}
    context['hello'] = '启动后台'
    return render(request, 'hello.html', context)

