from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework import status, generics
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import Task, Developer
from .serializers import TaskSerialzer, DeveloperSerialzer, UserSerializer, GroupSerializer, PermissionSerializer
from rest_framework.decorators import api_view

from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.models import User, Group, Permission

from sgqlc.operation import Operation
from sgqlc.endpoint.http import HTTPEndpoint
from .graphql_sgqlc import Query


# Create your views here.

@api_view(['GET'])
def task_list(request):

    query = Operation(Query)
    query.allTasks()
    endpoint = HTTPEndpoint(url='http://localhost:8000/graphql/')
    print(endpoint)
    result = endpoint(query=query)
    print("result: ")
    print(result)

    return JsonResponse(result)

    # if request.method == 'GET':
    #     tasks = Task.objects.all()
    #
    #     task_serializer = TaskSerialzer(tasks, many=True)
    #     return JsonResponse(task_serializer.data, safe=False)


@api_view(['GET'])
def task_detail(request, pk):

    query = Operation(Query)
    query.taskNode(id=str(pk))
    query.taskNode.edges()
    query.taskNode.page_info()

    endpoint = HTTPEndpoint(url='http://localhost:8000/graphql/')
    result = endpoint(query=query)

    return JsonResponse(result)

    # try:
    #     specific_task = Task.objects.get(id=pk)
    # except ObjectDoesNotExist:
    #     return JsonResponse({'message': 'The task does not exist'}, status=status.HTTP_404_NOT_FOUND)
    #
    # if request.method == 'GET':
    #     specific_task = Task.objects.get(id=pk)
    #     specific_task_serialzer = TaskSerialzer(specific_task)
    #     return JsonResponse(specific_task_serialzer.data)


@api_view(['GET'])
def developer_list(request):

    query = Operation(Query)
    query.allDevelopers()
    endpoint = HTTPEndpoint(url='http://localhost:8000/graphql/')
    print(endpoint)
    result = endpoint(query=query)
    print("result: ")
    print(result)

    return JsonResponse(result)

    # if request.method == 'GET':
    #     developers = Developer.objects.all()
    #
    #     developer_serializer = DeveloperSerialzer(developers, many=True)
    #     return JsonResponse(developer_serializer.data, safe=False)


@api_view(['GET'])
def developer_detail(request, pk):

    # try:
    #     specific_developer = Developer.objects.get(id=pk)
    # except ObjectDoesNotExist:
    #     return JsonResponse({'message': 'This developer does not exist'}, status=status.HTTP_404_NOT_FOUND)
    #
    # if request.method == 'GET':
    #     specific_developer = Developer.objects.get(id=pk)
    #     specific_developer_serialzer = DeveloperSerialzer(specific_developer)
    #     return JsonResponse(specific_developer_serialzer.data)

    query = Operation(Query)
    query.developerNode(id=str(pk))
    query.developerNode.edges()

    print(query)

    endpoint = HTTPEndpoint(url='http://localhost:8000/graphql/')
    print(endpoint)
    result = endpoint(query=query)
    print(result)

    return JsonResponse(result)


@api_view(['GET'])
def user_view(request):
    user_list = User.objects.all()
    user_serializer = UserSerializer(user_list)
    return JsonResponse(user_serializer.data)


@api_view(['GET'])
def group_view(request):
    group_list = Group.objects.all()
    group_serializer = GroupSerializer(group_list)
    return JsonResponse(group_serializer.data)


@api_view(['GET'])
def permission_view(request):
    permission_list = Permission.objects.all()
    permission_serializer = PermissionSerializer(permission_list)
    return JsonResponse(permission_serializer.data)