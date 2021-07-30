# Other libraries
# Graphene imports
import graphene

# Atom platform
from atomator.graphql.utils import GQL_ID

from ..models import Build
from .query import GQLBuild

# ToDo: protect this endpoint


class ReleaseBuild(graphene.Mutation):
    build = graphene.Field(GQLBuild)
    error = graphene.String()

    class Arguments:
        build_id = GQL_ID(required=True)

    @staticmethod
    def mutate(parent, info, build_id, **kwargs):
        build = Build.objects.get(id=build_id)
        build.release = True
        build.save()
        return ReleaseBuild(build=build)


class Mutation(graphene.ObjectType):
    release_build = ReleaseBuild.Field()
