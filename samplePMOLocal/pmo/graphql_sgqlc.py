from sgqlc.types.relay import Node, Connection, connection_args
from sgqlc.types import String, Type, Field, list_of

# Task

class TaskNode(Node):
    id = String
    name = String
    description = String


class TaskEdge(Type):
    node = Field(TaskNode)


class TaskConnection(Connection):
    edges = list_of(TaskEdge)


# Developer
class DeveloperNode(Node):
    id = String
    name = String
    position = String
    task = TaskNode
    # task = TaskNode


class DeveloperEdge(Type):
    node = Field(DeveloperNode)


class DeveloperConnection(Connection):
    edges = list_of(DeveloperEdge)


# Query
class Query(Type):
    allTasks = Field(TaskNode)
    taskNode = Field(
        TaskConnection,
        args={
            'id': String,
            'name': String,
            'description': String,
            **connection_args()
        }
    )

    developerNode = Field(DeveloperConnection, args={'id': str, 'name': str, 'position': str, 'task': TaskNode})

    # allDevelopers = Field(DeveloperType)
    # developerNode = Field(
    #     DeveloperConnection,
    #     args = {
    #         'id': String,
    #         'name': String,
    #         'position': String,
    #         # 'task': TaskNode,
    #         'task': String,
    #         **connection_args()
    #     }
    # )