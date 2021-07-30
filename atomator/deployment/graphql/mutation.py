# Other libraries
# Graphene imports
import graphene

# Atom platform
from atomator.graphql.utils import GQL_ID, is_logged
from atomator.version_manager.models import Build

from ..models import (
    ConfigEnvironment,
    EnvironmentChoices,
    ExecutionOutput,
    OutputChoices,
)
from ..tasks import start_deployment


class StartDeploy(graphene.Mutation):
    results_id = GQL_ID()

    class Arguments:
        build_id = GQL_ID(required=True)
        environment_id = GQL_ID(required=True)

    @staticmethod
    @is_logged
    def mutate(parent, info, build_id, environment_id, **kwargs):
        build = Build.objects.get(id=build_id)
        environment = ConfigEnvironment.objects.get(id=environment_id)
        # ToDo: Check if build and environment can match
        print(build, environment)
        print(build.release)
        if (
            not build.release
            and environment.environment == EnvironmentChoices.production
        ):
            return {"results_id": -1}
        output = ExecutionOutput.objects.create(
            status=OutputChoices.pending,
            environment=environment,
            build=build,
            application=build.application,
        )
        start_deployment.delay(output.id)
        return {"results_id": output.id}


class Mutation(graphene.ObjectType):
    start_deploy = StartDeploy.Field()
