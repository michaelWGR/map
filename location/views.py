from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Keymsg, Traffic_info, Circle, Transit_detail
from .best_location import *
import json



def index(request):
    key_list = Keymsg.objects.all().order_by('id')
    context = {
        'key_list': key_list,
    }
    return render(request, 'location/index.html', context)

def locate(request):
    key_list = Keymsg.objects.all().order_by('id')
    context = {
        'key_list': key_list,
    }
    if request.method == 'GET':
        address = request.GET.get('address')
        city = request.GET.get('city')
        key = request.GET.get('key')
        lo = get_location(address=address, city=city, key=key)
        if lo:
            full_address_list = get_regeo(location=lo, key=key)
            context['full_address_list'] = full_address_list
            context['location'] = lo
    return render(request, 'location/index.html', context)

def transit_direction(request):
    key_list = Keymsg.objects.all().order_by('id')
    context = {
        'key_list': key_list,
    }
    if request.method == 'POST':
        location1 = request.POST.get('location1')
        location2 = request.POST.get('location2')
        key = request.POST.get('key')

        circle = get_circle(location1=location1, location2=location2, key=key)
        if circle:
            center_location = circle[0]
            radius = circle[1]
            # circle = get_object_or_404(Circle, center_location=center_location, radius=radius)
            circle_queryset = Circle.objects.filter(center_location=center_location, radius=radius)
            if not circle_queryset:
                c = Circle(center_location=center_location, radius=radius)
                c.save()
                circle = c
            else:
                circle = circle_queryset[0]

            traffic_list = get_around_place(location=center_location, radius=radius, key=key)
            for traffic in traffic_list:
                name = traffic['name']
                location = traffic['location']
                traffic_info_filter = Traffic_info.objects.filter(name=name, location=location, circle=circle)
                if not traffic_info_filter:
                    t = Traffic_info(name=name, location=location, circle=circle)
                    t.save()
                else:
                    t = traffic_info_filter[0]

                transit_detail_filter = Transit_detail.objects.filter(traffic_info=t)
                if not transit_detail_filter:
                    transit_detail = aggregate_target_info(key, location1, location2, **traffic)
                    if transit_detail:
                        total_per_cost = transit_detail['total_per_cost']
                        total_per_duration = transit_detail['total_per_duration']
                        total_per_walking_distance = transit_detail['total_per_walking_distance']
                        total_per_distance = transit_detail['total_per_distance']
                        detail = json.dumps(transit_detail['detail'])
                        around_market = json.dumps(transit_detail['around_market'])
                        around_housing = json.dumps(transit_detail['around_housing'])

                        td = Transit_detail(total_per_cost=total_per_cost, total_per_duration=total_per_duration,
                                           total_per_walking_distance=total_per_walking_distance, total_per_distance=total_per_distance,
                                           detail=detail, around_market=around_market, around_housing=around_housing,
                                           traffic_info=t)
                        td.save()

            traffic_info = Traffic_info.objects.filter(circle=circle)
            context['traffic_info'] = traffic_info

    return render(request, 'location/index.html', context)

def detail(request, traffic_info_id):
    # transit_detail_by_id = Transit_detail.objects.filter(traffic_info_id=traffic_info_id)
    transit_detail_by_id = get_object_or_404(Transit_detail, traffic_info_id=traffic_info_id)
    transit_detail_by_id.detail = json.loads(transit_detail_by_id.detail)
    transit_detail_by_id.around_market = json.loads(transit_detail_by_id.around_market)
    transit_detail_by_id.around_housing = json.loads(transit_detail_by_id.around_housing)
    context = {
        'transit_detail': transit_detail_by_id
    }

    return render(request, 'location/detail.html', context)


