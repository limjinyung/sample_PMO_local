from rest_framework import serializers
from .models import Task, Developer
from django.contrib.auth.models import User, Group, Permission


class TaskSerialzer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('id', 'name','description')


class DeveloperSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = ('id', 'name', 'task', 'position')


class UserSerializer(serializers.ModelSerializer):
    # permissions = serializers.PrimaryKeyRelatedField(many=True, queryset=Permission.objects.all())

    class Meta:
        model = User
        fields = ('username', 'email', 'permissions', 'isStaff')
        # fields = ('username', 'email', 'is_staff')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', 'permissions')


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('name', 'content_type')
