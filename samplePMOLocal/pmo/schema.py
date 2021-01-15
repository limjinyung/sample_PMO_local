import graphene
from graphene_django import DjangoObjectType

from .models import Task, Developer
from django.contrib.auth.models import User, Group, Permission


class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        fields = "__all__"


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
    class Meta:
        model = Developer
        fields = "__all__"


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
    all_tasks = graphene.List(TaskType)
    task = graphene.List(TaskType, id=graphene.String())

    all_developers = graphene.List(DeveloperType)
    developer = graphene.List(DeveloperType, id=graphene.String())

    users = graphene.List(UserType)
    user_search = graphene.List(UserType, id=graphene.String())

    groups = graphene.List(GroupType)
    group_search = graphene.List(GroupType, id=graphene.String())

    permission = graphene.List(PermissionType)
    permission_search = graphene.List(PermissionType, id=graphene.String())

    def resolve_all_tasks(self, info, **kwargs):
        return Task.objects.all()

    def resolve_task(self, info, **kwargs):
        id = kwargs.get("id", "")
        return Task.objects.filter(id=id)

    def resolve_all_developers(self, info, **kwargs):
        return Developer.objects.all()

    def resolve_developer(self, info, **kwargs):
        id = kwargs.get("id", "")
        return Developer.objects.filter(id=id)

    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_user_search(self, info, **kwargs):
        id = kwargs.get("id", "")
        return User.objects.filter(id=id)

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