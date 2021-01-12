import graphene

import pmo.schema as pmo_schema

class Query(pmo_schema.Query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)