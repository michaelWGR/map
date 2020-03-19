from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Keymsg, Traffic_info, Circle, Transit_detail
from .best_location import *
import json



def index(request):
    key_list = Keymsg.objects.all().order_by('id')
    context = {
        'key_list': key_list,
    }
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

@csrf_exempt
def search_location(request):
    context = {}
    if request.method == 'GET':
        address = request.GET.get('address')
        city = request.GET.get('city')
        key = request.GET.get('key')
        lo = get_location(address=address, city=city, key=key)
        if lo:
            full_address_list = get_regeo(location=lo, key=key)
            context['full_address_list'] = full_address_list
            context['location'] = lo
            context['code'] = 0

        else:
            context = {
                'code': 1,
                'error': 'cannot get location!'
            }

    else:
        context = {
            'code': 1,
            'error': 'method is wrong!'
        }
    return JsonResponse(context)

@csrf_exempt
def search_transit_direction(request):
    context = {}
    try:
        if request.method == 'POST':
            location1 = request.POST.get('location1')
            location2 = request.POST.get('location2')
            key = request.POST.get('key')
            order_name = request.POST.get('order_name')
            order_type = request.POST.get('order_type')
            page_num = int(request.POST.get('page_num')) if request.POST.get('page_num') != "" else 1
            page_size = int(request.POST.get('page_size')) if request.POST.get('page_size') != "" else 10

            circle_tuple = get_circle(location1=location1, location2=location2, key=key)
            if circle_tuple:
                center_location = circle_tuple[0]
                radius = circle_tuple[1]
                circle_queryset = Circle.objects.filter(center_location=center_location, radius=radius)
                if not circle_queryset:
                    c = Circle(center_location=center_location, radius=radius)
                    c.save()
                    circle = c
                else:
                    circle = circle_queryset[0]

                traffic_list = get_around_place(location=center_location, radius=radius, key=key)
                try:
                    for traffic in traffic_list:
                        name = traffic['name']
                        location = traffic['location']
                        traffic_info_filter = Traffic_info.objects.filter(name=name, location=location, circle=circle)
                        if not traffic_info_filter:
                            t = Traffic_info(name=name, location=location, circle=circle)
                            t.save()
                        else:
                            t = traffic_info_filter[0]

                        print(t)
                        transit_detail_filter = Transit_detail.objects.filter(traffic_info=t, circle=circle)
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
                                                   traffic_info=t, circle=circle)
                                td.save()


                    order_method = order_type+order_name
                    transit_detail_queryset = Transit_detail.objects.filter(circle=circle)\
                        .values('traffic_info_id', 'traffic_info__name', 'total_per_cost', 'total_per_duration', 'total_per_walking_distance', 'total_per_distance').order_by(order_method)

                    p = Paginator(transit_detail_queryset, page_size)
                    current_page = p.page(page_num)

                    transit_detail_list = []
                    for i in current_page.object_list:
                        transit_detail_list.append(i)

                    context = {
                        'code': 0,
                        'transit_detail': transit_detail_list,
                        'has_previous': current_page.has_previous(),
                        'has_next': current_page.has_next(),
                        'num_pages': p.num_pages
                    }
                except Exception as e:
                    print('inner' + str(e))
                    context = {
                        'code': 1,
                        'error': str(e)
                    }
        else:
            context = {
                'code': 1,
                'error': 'method is wrong!'
            }
        # return JsonResponse(context)
    except Exception as e:
        context = {
            'code': 1,
            'error': str(e)
        }
        print(e)
    return JsonResponse(context)