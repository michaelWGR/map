from django.shortcuts import render
from django.http import HttpResponse
from .models import Keymsg
from .best_location import get_location

def index(request):
    key_list = Keymsg.objects.all().order_by('id')
    context = {
        'title': 'map for you',
        'key_list': key_list,
    }
    return render(request, 'location/index.html', context)


