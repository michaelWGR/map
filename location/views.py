from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Keymsg, Traffic_info, Circle, Transit_detail
from .best_location import *
import json



def index(request):
    key_list = Keymsg.objects.filter(is_deleted=0).order_by('id')
    context = {
        'key_list': key_list,
    }
    return render(request, 'location/index.html', context)

def detail(request, traffic_info_id):
    transit_detail_by_id = get_object_or_404(Transit_detail, traffic_info_id=traffic_info_id)
    transit_detail_by_id.detail = json.loads(transit_detail_by_id.detail)
    transit_detail_by_id.around_market = json.loads(transit_detail_by_id.around_market)
    transit_detail_by_id.around_housing = json.loads(transit_detail_by_id.around_housing)
    context = {
        'transit_detail': transit_detail_by_id
    }
    return render(request, 'location/detail.html', context)

def db_data(request):
    circle_list = Circle.objects.all().order_by('-modified_time')
    traffic_info_list = Traffic_info.objects.all().order_by('-modified_time')
    transit_detail_list= Transit_detail.objects.all().order_by('-modified_time')
    context = {
        'circle_list': circle_list,
        'traffic_info_list': traffic_info_list,
        'transit_detail_list': transit_detail_list
    }
    return render(request, 'location/db_data.html', context)

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

                #查询并插入circle数据
                circle_queryset = Circle.objects.filter(center_location=center_location, radius=radius)
                if not circle_queryset:
                    c = Circle(center_location=center_location, radius=radius)
                    c.save()
                circle = Circle.objects.filter(center_location=center_location, radius=radius)[0]
                print('circle_id: {}'.format(circle.id))

                # 查询并插入traffic_info数据
                traffic_info_filter = Traffic_info.objects.filter(circle=circle)
                if not traffic_info_filter:
                    traffic_list = get_around_place(location=center_location, radius=radius, key=key)
                    for traffic in traffic_list:
                        name = traffic['name']
                        location = traffic['location']
                        t = Traffic_info(name=name, location=location, circle=circle)
                        t.save()
                    print(traffic_list)

                # 查询并插入transit_detail数据
                transit_detail_filter = Transit_detail.objects.filter(circle=circle)
                if not transit_detail_filter:
                    traffic_info_filter = Traffic_info.objects.filter(circle=circle)
                    for traffic_info_object in traffic_info_filter:
                        traffic = {
                            'name': traffic_info_object.name,
                            'location': traffic_info_object.location
                        }
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
                                                total_per_walking_distance=total_per_walking_distance,
                                                total_per_distance=total_per_distance,
                                                detail=detail, around_market=around_market, around_housing=around_housing,
                                                traffic_info=traffic_info_object, circle=circle)
                            td.save()
                            print(traffic_info_object.name)
                        else:
                            context = {
                                'code': 1,
                                'error': 'sorry,it is wrong to get target info and traffic_info is {}'.format(traffic)
                            }
                            return JsonResponse(context)

                # 分页展示数据
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

            else:
                context = {
                    'code': 1,
                    'error': 'It is wrong to get circle info!'
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

@csrf_exempt
def delete_data(request):
    if request.method == 'POST':
        try:
            circle_id = request.POST.get('circle_id')
            db_table_name = request.POST.get('db_table_name')
            if not circle_id.isdigit():
                context = {
                    'code': 1,
                    'error': 'circle_id is not number.'
                }
                return JsonResponse(context)
            else:
                rp = ()
                if db_table_name == 'location_circle':
                    rp = Circle.objects.filter(id=circle_id).delete()
                elif db_table_name == 'location_traffic_info':
                    rp = Traffic_info.objects.filter(circle_id=circle_id).delete()
                elif db_table_name == 'location_transit_detail':
                    rp = Transit_detail.objects.filter(circle_id=circle_id).delete()

                context = {
                    'code': 0,
                    'delete_count': rp[0],
                    'delete_msg': rp[1]
                }
                return JsonResponse(context)
        except Exception as e:
            context = {
                'code': 1,
                'error': str(e)
            }
            return JsonResponse(context)
    else:
        context = {
            'code': 1,
            'error': 'method is wrong!'
        }
        return JsonResponse(context)