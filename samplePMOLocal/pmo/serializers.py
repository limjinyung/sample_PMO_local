from rest_framework import serializers
from .models import Task, Developer


class TaskSerialzer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('name','description')


class DeveloperSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = ('name', 'task', 'position')