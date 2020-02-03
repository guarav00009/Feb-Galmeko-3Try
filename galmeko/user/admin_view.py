from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
from setting.models import Vehicle
from vendor.models import Driver
from django.contrib import messages
from django.core import serializers
import json
import os
from .models import User

# Get Vehicle list for vendor DataTable
def get_vehicle_list(request):
    vendor_id = request.POST.get('vendor_id')
    draw = int(request.GET.get("draw", 0))
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 7))

    all_objects = Vehicle.objects.filter(vendor_id=vendor_id)
    filtered_count = all_objects.count()
    total_count = Vehicle.objects.count()
    data = serializers.serialize('json', all_objects)

    json_objects = json.loads(data)
    list_objects = []
    for index in range(len(json_objects)):
        json_objects[index]['fields']['id'] = all_objects[index].id
        json_objects[index]['fields']['status_id'] = all_objects[index].status
        result = json_objects[index]['fields']['status']
        if(result == 1):
            json_objects[index]['fields']['status'] = 'Active'
        elif(result == 0):
            json_objects[index]['fields']['status'] = 'Inactive'
        elif(result == 2):
            json_objects[index]['fields']['status'] = 'Booked'
        else:
            json_objects[index]['fields']['status'] = 'Deleted'
        list_objects.append(json_objects[index]['fields'])

    return HttpResponse(json.dumps(list_objects), content_type='application/json;charset=utf-8')

# Delete Functionality for vehicle Listing on vendor
def delete_vehicle(request):
    result = {}
    if request.method == 'POST' and request.is_ajax():
        try:
            vehicleId = request.POST.get('id', '')
            response = Vehicle.objects.filter(pk=vehicleId).update(status=3)
            if (response == True):
                result['status'] = True
                result['msg'] = 'Vehicle Deleted Successfully successfully!'
                return JsonResponse(result)
            else:
                result['status'] = False
                result['msg'] = 'Something went wrong!'
                return JsonResponse(result)
        except Http404:
            return HttpResponseRedirect("/vendor/vendor/view/")
    else:
        return HttpResponse('Invalid request passed')

# Driver Listing for Vendor Section
def get_driver_list(request):
    vendor_id = request.POST.get('vendor_id')
    print(vendor_id)
    draw = int(request.GET.get("draw", 0))
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 7))

    all_objects = Driver.objects.filter(vendor_id=vendor_id)
    filtered_count = all_objects.count()
    total_count = Driver.objects.count()
    data = serializers.serialize('json', all_objects)

    json_objects = json.loads(data)
    list_objects = []
    for index in range(len(json_objects)):
        json_objects[index]['fields']['id'] = all_objects[index].id
        json_objects[index]['fields']['status_id'] = all_objects[index].status
        result = json_objects[index]['fields']['status']
        if(result == 1):
            json_objects[index]['fields']['status'] = 'Active'
        elif(result == 0):
            json_objects[index]['fields']['status'] = 'Inactive'
        elif(result == 2):
            json_objects[index]['fields']['status'] = 'Booked'
        else:
            json_objects[index]['fields']['status'] = 'Deleted'
        list_objects.append(json_objects[index]['fields'])

    return HttpResponse(json.dumps(list_objects), content_type='application/json;charset=utf-8')