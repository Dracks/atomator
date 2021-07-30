# Other libraries
# Graphene imports
import graphene
from graphene_django.types import DjangoObjectType

# Atom platform
from atomator.graphql.utils import GQL_ID, is_logged
from atomator.version_manager.graphql.query import GQLBuild

from ..models import Application, Repository, Token


class GQLRepository(DjangoObjectType):
    class Meta:
        model = Repository


class GQLToken(DjangoObjectType):
    class Meta:
        model = Token
        exclude = ("application",)


class GQLApplication(DjangoObjectType):
    id = GQL_ID(required=True)
    last_release = graphene.Field(GQLBuild)
    last_build = graphene.Field(GQLBuild)

    class Meta:
        model = Application

    def resolve_last_release(self, info):
        qs = self.build_set.filter(release=True)
        if qs.count():
            return qs.first()

    def resolve_last_build(self, info):
        qs = self.build_set
        if qs.count():
            return qs.first()


class Query(graphene.ObjectType):
    applications = graphene.List(graphene.NonNull(GQLApplication), required=True)

    @staticmethod
    @is_logged
    def resolve_applications(parent, info):
        return Application.objects.all()
