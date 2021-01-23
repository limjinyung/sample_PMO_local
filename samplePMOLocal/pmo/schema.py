import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from .models import Task, Developer
from django.contrib.auth.models import User, Group, Permission

import django_filters
from graphene_django.filter import DjangoFilterConnectionField

POSITIONS = (
        ('PM', 'Project Manager'),
        ('QA', 'Quality Assurance'),
        ('SD', 'Software Developer'),
)


class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        filter_fields = {
            'name': ['exact','icontains','istartswith'],
            'description': ['exact', 'icontains', 'istartswith']
        }
        interfaces = (relay.Node,)


class CreateTask(graphene.Mutation):
    class Arguments:
        # input arguments for this mutations
        name = graphene.String(required=True)
        description = graphene.String()

    ok = graphene.Boolean()
    task = graphene.Field(TaskType)

    @classmethod
    def mutate(cls, root, info, name, description):
        task = Task(name=name, description=description)
        ok = True
        task.save()
        return CreateTask(task=task, ok=ok)


class UpdateTask(graphene.Mutation):
    class Arguments:
        id = graphene.String()
        name = graphene.String()
        description = graphene.String()

    task = graphene.Field(TaskType)

    @classmethod
    def mutate(cls, root, info, id, name=None, description=None):
        task = Task.objects.get(id=id)
        task.name = name if name is not None else task.name
        task.description = description if description is not None else task.description

        task.save()

        return UpdateTask(task=task)


class DeleteTask(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    task = graphene.Field(TaskType)

    def mutate(cls, root, id):
        task = Task.objects.get(id=id)
        if task is not None:
            task.delete()

        return DeleteTask(task=task)


class DeveloperType(DjangoObjectType):
    task = graphene.List(TaskType)

    @graphene.resolve_only_args
    def resolve_task(self):
        return self.task.all()

    class Meta:
        model = Developer
        filter_fields = {
            'name': ['exact','icontains','istartswith'],
            'task': ['exact']
        }
        interfaces = (relay.Node,)


class CreateDeveloper(graphene.Mutation):
    class Arguments:
        # input arguments for this mutations
        name = graphene.String(required=True)
        task_list = graphene.List(graphene.Int)
        position = graphene.String()

    ok = graphene.Boolean()
    developer = graphene.Field(DeveloperType)

    @classmethod
    def mutate(cls, root, info, name, task_list, position):

        if not any(position in i for i in POSITIONS):
            raise Exception('Invalid position!')

        developer = Developer.objects.create(name=name, position=position)

        for task in task_list:
            input_task = Task.objects.get(id=task)
            developer.task.add(input_task)
        ok = True
        developer.save()

        return CreateDeveloper(developer=developer, ok=ok)


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = "__all__"


class AddPermission(graphene.Mutation):
    class Arguments:
        id = graphene.String()
        permission_id = graphene.String()

    user = graphene.Field(UserType)

    def mutate(cls, root, id, permission_id=None):
        user = User.objects.get(id=id)

        if permission_id is not None:
            permission = Permission.objects.get(id=permission_id)
            user.user_permissions.add(permission)
            user.save()

        return AddPermission(user=user)


class DeletePermission(graphene.Mutation):
    class Arguments:
        id = graphene.String()
        permission_id = graphene.String()

    user = graphene.Field(UserType)

    def mutate(cls, root, id, permission_id=None):
        user = User.objects.get(id=id)

        if permission_id is not None:
            permission = Permission.objects.get(id=permission_id)
            user.user_permissions.remove(permission)
            user.save()

        return DeletePermission(user=user)


class GroupType(DjangoObjectType):
    class Meta:
        model = Group
        fields = "__all__"


class PermissionType(DjangoObjectType):
    class Meta:
        model = Permission
        fields = "__all__"


class Query(graphene.ObjectType):

    all_tasks = graphene.List(TaskType, first=graphene.Int(), orderBy=graphene.List(of_type=graphene.String))
    task = graphene.List(TaskType, id=graphene.String(), name=graphene.String())
    task_node = DjangoFilterConnectionField(TaskType, id=graphene.String())

    all_developers = graphene.List(DeveloperType)
    developer = graphene.List(DeveloperType, id=graphene.String(), name=graphene.String())
    developer_node = DjangoFilterConnectionField(DeveloperType, id=graphene.String())

    users = graphene.List(UserType)
    user_search = graphene.List(UserType, id=graphene.String())

    groups = graphene.List(GroupType)
    group_search = graphene.List(GroupType, id=graphene.String())

    permission = graphene.List(PermissionType)
    permission_search = graphene.List(PermissionType, id=graphene.String())

    def resolve_all_tasks(self, info, first=None, **kwargs): # first = None
        ts = Task.objects.all()

        orderBy = kwargs.get('orderBy', None)

        if first:
            ts = ts[:first]

        if orderBy:
            return Task.objects.order_by(*orderBy)

        return ts

    def resolve_task(self, info, **kwargs):
        id = kwargs.get("id", "")
        return Task.objects.filter(id=id)

    def resolve_task_node(self, info, **kwargs):
        id = kwargs.get("id","")
        return Task.objects.filter(id=id)

    def resolve_all_tasks(root, info, **kwargs):
        return Task.objects.all()

    def resolve_all_developers(self, info, **kwargs):
        return Developer.objects.all()

    def resolve_developer(self, info, **kwargs):
        id = kwargs.get("id", "")
        name = kwargs.get("name", "")
        return Developer.objects.filter(id=id, name=name)

    def resolve_developer_node(self, info, **kwargs):
        id = kwargs.get("id","")
        return Developer.objects.filter(id=id)

    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_user_search(self, info, **kwargs):
        id = kwargs.get("id", "")
        name = kwargs.get("name", "")
        return User.objects.filter(id=id, name=name)

    def resolve_groups(self, info, **kwargs):
        return Group.objects.all()

    def resolve_group_search(self, info, **kwargs):
        id = kwargs.get("id", "")
        return Group.objects.filter(id=id)

    def resolve_permission(self, info, **kwargs):
        return Permission.objects.all()

    def resolve_permission_search(self, info, **kwargs):
        id = kwargs.get("id", "")
        return Permission.objects.filter(id=id)


class Mutation(graphene.ObjectType):
    create_task = CreateTask.Field()
    update_task = UpdateTask.Field()
    delete_task = DeleteTask.Field()

    add_permission = AddPermission.Field()
    delete_permission = DeletePermission.Field()

    create_developer = CreateDeveloper.Field()