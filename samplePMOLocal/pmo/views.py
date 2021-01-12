from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from .models import Task, Developer
from .serializers import TaskSerialzer, DeveloperSerialzer
from rest_framework.decorators import api_view

from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
@api_view(['GET'])
def pmo_list(request):
    if request.method == 'GET':
        tasks = Task.objects.all()

        task_serializer = TaskSerialzer(tasks, many=True)
        return JsonResponse(task_serializer.data, safe=False)


@api_view(['GET'])
def pmo_detail(request,pk):

    try:
        specific_task = Task.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return JsonResponse({'message': 'The task does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        specific_task = Task.objects.get(pk=pk)
        return JsonResponse(specific_task.data)