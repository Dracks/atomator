# Other libraries
# Graphene imports
import graphene
from graphene_django.types import DjangoObjectType

# Atom platform
from atomator.graphql.utils import GQL_ID, is_logged
from atomator.version_manager.models import Build

from ..models import (
    HASH_ENVIRONMENTS,
    HASH_OUTPUT_CHOICES,
    HASH_TASK_STATUS,
    ConfigEnvironment,
    DeploymentConfiguration,
    ExecutionError,
    ExecutionOutput,
    Machine,
    Tag,
    TaskOutput,
)


class GQLMachine(DjangoObjectType):
    class Meta:
        model = Machine
        fields = ("id", "name")


class GQLConfigTag(DjangoObjectType):
    class Meta:
        model = Tag


class GQLEnvironmentType(graphene.Enum):
    devel = "Development"
    staging = "Staging"
    production = "Production"


class GQLTaskStatusType(graphene.Enum):
    nothing_done = "Nothing done"
    changed = "Changed"
    error = "Error"
    unreachable = "Unreachable"


class GQLExecutionStatusType(graphene.Enum):
    pending = "Pending"
    working = "Working"
    ok = "OK"
    error = "Error"


class GQLConfigEnvironment(DjangoObjectType):
    environment = graphene.Field(GQLEnvironmentType)

    class Meta:
        model = ConfigEnvironment

    def resolve_environment(self, info):
        return HASH_ENVIRONMENTS[self.environment]


class GQLAppConfig(DjangoObjectType):
    id = GQL_ID(required=True)

    class Meta:
        model = DeploymentConfiguration


class GQLExecutionOutput(DjangoObjectType):
    id = GQL_ID(required=True)
    status = graphene.Field(GQLExecutionStatusType, required=True)

    def resolve_status(self, info):
        return HASH_OUTPUT_CHOICES[self.status]

    class Meta:
        model = ExecutionOutput


class GQLExecutionError(DjangoObjectType):
    id = GQL_ID(required=True)

    class Meta:
        model = ExecutionError
        exclude = ("execution",)


class GQLTaskOutput(DjangoObjectType):
    id = GQL_ID(required=True)
    status = graphene.Field(GQLTaskStatusType, required=True)
    app_name = graphene.String(required=True)

    def resolve_status(self, info):
        return HASH_TASK_STATUS[self.status]

    def resolve_app_name(self, info):
        return self.build.application.name

    class Meta:
        model = TaskOutput
        exclude = ("execution",)


class Query(graphene.ObjectType):
    deployments = graphene.List(
        graphene.NonNull(GQLExecutionOutput),
        deploy_id=GQL_ID(),
        from_dt=graphene.DateTime(),
    )

    @is_logged
    def resolve_deployments(self, info, deploy_id=None, from_dt=None):
        if deploy_id:
            return [ExecutionOutput.objects.get(id=deploy_id)]
        else:
            qs = ExecutionOutput.objects.all()
            if from_dt:
                qs = qs.filter(date__lt=from_dt)
            return qs[:20]
