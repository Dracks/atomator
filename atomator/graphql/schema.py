# Other libraries
# Graphene imports
import graphene

# Atom platform
from atomator.application.graphql.query import Query as ApplicationQuery
from atomator.deployment.graphql import Mutation as DepMutation
from atomator.deployment.graphql import Query as DepQuery
from atomator.version_manager.graphql.mutation import Mutation as VMMutation
from atomator.version_manager.graphql.query import Query as VMQuery

from .profile.mutations import Mutation as ProfileMutation
from .profile.query import Query as ProfileQuery


class Query(ProfileQuery, DepQuery, VMQuery, ApplicationQuery, graphene.ObjectType):
    pass


class Mutation(VMMutation, DepMutation, ProfileMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
