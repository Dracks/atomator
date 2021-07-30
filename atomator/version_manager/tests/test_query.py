# Standard Library
import json

# Django imports
from django.contrib.auth import get_user_model

# Graphene imports
from graphene_django.utils.testing import GraphQLTestCase

# Atom platform
from atomator.application.models import Application
from atomator.graphql.utils_test import graphQlTest

from ..graphql.mutation import Mutation
from ..graphql.query import Query
from ..models import Build, ChangesChoices

LAST_BUILDS = """
query GetLatestBuilds{
  lastBuilds{
    id,
    application{
        id,
        name,
    }
    major,
    minor,
    patch,
    release,
    isReleasable,
    branch,
    date,
    file {
        size,
        name,
        url,
    }
  }
}
"""


@graphQlTest(query=Query, mutation=Mutation)
class TestLastBuilds(GraphQLTestCase):
    fixtures = ["application.yaml"]

    def setUp(self):
        User = get_user_model()
        admin = User.objects.create(
            username="admin", is_staff=True, is_active=True, is_superuser=True
        )
        admin.set_password("pwd")
        admin.save()
        self._client.login(username="admin", password="pwd")
        self.build = Build.objects.create(
            application=Application.objects.get(pk=1),
            major=0,
            minor=0,
            patch=0,
            commit="asdf",
            release=False,
            branch="main",
            change=ChangesChoices.minor,
        )

    def test_last_builds_diferent_branch(self):

        response = self.query(LAST_BUILDS)

        self.assertResponseNoErrors(response)

        content = json.loads(response.content)
        self.assertEqual(
            content.get("data", {}).get("lastBuilds", []),
            [
                {
                    "id": self.build.pk,
                    "application": {"id": 1, "name": "hola mundo",},
                    "major": 0,
                    "minor": 0,
                    "patch": 0,
                    "release": False,
                    "isReleasable": False,
                    "branch": "main",
                    "date": self.build.date.isoformat(),
                    "file": None,
                }
            ],
        )

    def test_last_builds_same_branch(self):
        self.build.branch = "release"
        self.build.save()

        response = self.query(LAST_BUILDS)

        self.assertResponseNoErrors(response)

        content = json.loads(response.content)
        self.assertEqual(
            content.get("data", {}).get("lastBuilds", []),
            [
                {
                    "id": self.build.pk,
                    "application": {"id": 1, "name": "hola mundo",},
                    "major": 0,
                    "minor": 0,
                    "patch": 0,
                    "release": False,
                    "isReleasable": True,
                    "branch": "release",
                    "date": self.build.date.isoformat(),
                    "file": None,
                }
            ],
        )

    def test_last_builds_same_branch_released(self):
        self.build.branch = "release"
        self.build.release = True
        self.build.save()

        response = self.query(LAST_BUILDS)

        self.assertResponseNoErrors(response)

        content = json.loads(response.content)
        self.assertEqual(
            content.get("data", {}).get("lastBuilds", []),
            [
                {
                    "id": self.build.pk,
                    "application": {"id": 1, "name": "hola mundo",},
                    "major": 0,
                    "minor": 0,
                    "patch": 0,
                    "release": True,
                    "isReleasable": False,
                    "branch": "release",
                    "date": self.build.date.isoformat(),
                    "file": None,
                }
            ],
        )
