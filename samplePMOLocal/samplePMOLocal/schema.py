import graphene
import pmo.schema as pmo_schema


class Task(graphene.ObjectType):
    name = graphene.String()
    description = graphene.String()


class PmoMutations(graphene.ObjectType):
    create_task = pmo_schema.CreateTask.Field()
    update_task = pmo_schema.UpdateTask.Field()
    delete_task = pmo_schema.DeleteTask.Field()

    add_permission = pmo_schema.AddPermission.Field()
    delete_permission = pmo_schema.DeletePermission.Field()

    create_developer = pmo_schema.CreateDeveloper.Field()


class Query(pmo_schema.Query, graphene.ObjectType):
    # task = graphene.Field(Task)
    pass


schema = graphene.Schema(query=Query, mutation=PmoMutations)


