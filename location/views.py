from django.shortcuts import render
from django.http import HttpResponse
from .models import Keymsg

def index(request):
    key_list = Keymsg.objects.all().order_by('-id')
    return render(request, 'location/index.html', context={
        'title': 'map for you',
        'key_list': key_list,
    })


