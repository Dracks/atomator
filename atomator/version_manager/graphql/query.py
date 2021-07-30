# Other libraries
# Django imports
from django.urls import reverse

# Graphene imports
import graphene
from graphene_django.types import DjangoObjectType

# Atom platform
from atomator.graphql.utils import GQL_ID, is_logged

from ..models import Build, Change, FileInfo


class GQLChangeType(graphene.Enum):
    fix = "fix"
    improvement = "imp"
    new_feature = "fea"
    unknown = "unk"


class GQLChange(DjangoObjectType):
    type = graphene.Field(GQLChangeType)

    class Meta:
        model = Change
        exclude = ("build",)


class GQLFileInfo(DjangoObjectType):
    url = graphene.String(required=True)

    def resolve_url(self, info):
        return reverse("download-version", args=[self.uuid])

    class Meta:
        model = FileInfo
        exclude = ("build", "file_name", "uuid")


class GQLBuild(DjangoObjectType):
    id = GQL_ID(required=True)
    is_releasable = graphene.Boolean(required=True)

    class Meta:
        model = Build

    def resolve_is_releasable(self, info):
        return self.branch == self.application.release_branch and not self.release


class Query(graphene.ObjectType):
    build_info = graphene.Field(GQLBuild, build_id=GQL_ID(required=True))
    last_builds = graphene.List(graphene.NonNull(GQLBuild),)

    @is_logged
    def resolve_build_info(self, info, build_id):
        return Build.objects.get(id=build_id)

    @is_logged
    def resolve_last_builds(self, info):
        return Build.objects.all()[:10]
