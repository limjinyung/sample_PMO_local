import graphene
from graphene_django import DjangoObjectType

from .models import Task, Developer


class TaskType(DjangoObjectType):
    class Meta:
        model = Task


class DeveloperType(DjangoObjectType):
    class Meta:
        model = Developer


class Query(graphene.ObjectType):
    tasks = graphene.List(TaskType)
    developers = graphene.List(DeveloperType)

    def resolve_tasks(self, info, **kwargs):
        return Task.objects.all()

    def resolve_developers(self, info, **kwargs):
        return Developer.objects.all()