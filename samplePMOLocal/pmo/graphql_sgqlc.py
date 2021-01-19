from sgqlc.types.relay import Node, Connection, connection_args
from sgqlc.types import String, Type, Field, list_of


class TaskNode(Type):
    id = String
    name = String
    description = String


class TaskEdge(Type):
    node = Field(TaskNode)


class TaskConnection(Connection):
    edges = list_of(TaskEdge)


class Query(Type):
    allTasks = Field(TaskNode)
    task = Field(
        TaskConnection,
        args={
            'id': String,
            'name': String,
            'description': String
        }
    )