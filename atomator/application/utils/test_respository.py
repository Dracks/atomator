# Django imports
# Standard Library
from unittest.mock import Mock, patch

from django.test import TestCase

from ..models import (
    Application,
    ProviderChoices,
    RepoApp,
    RepoAppIntValue,
    Repository,
    RepositoryStringValue,
)
from ..repository import GitlabRepository

# Create your tests here.


class TestGitlab(TestCase):
    def setUp(self):
        self.subject_app = Application.objects.create(name="Hyper App",)
        self.subject_repo = Repository.objects.create(
            provider=ProviderChoices.gitlab,
            name="Gitlab from Hyper App",
            url="http://url.app",
        )
        RepositoryStringValue.objects.create(
            repository=self.subject_repo,
            key="token",
            value="this is an important token",
        )

        link = RepoApp.objects.create(
            repository=self.subject_repo, application=self.subject_app,
        )

        RepoAppIntValue.objects.create(repo_app=link, key="project_id", value=42)

        self.subject = GitlabRepository(self.subject_app, self.subject_repo)

    def tearDown(self):
        RepoApp.objects.all().delete()
        Repository.objects.all().delete()
        Application.objects.all().delete()

    def test_create_tag(self):
        hash_commit = "9876789"
        response = Mock()
        response.status_code = 201
        with patch("requests.post") as patched_post:
            patched_post.return_value = response
            self.subject.create_tag("tag_name", hash_commit)

            headers = {"PRIVATE-TOKEN": "this is an important token"}
            params = {"tag_name": "tag_name", "ref": hash_commit}
            patched_post.assert_called_once_with(
                "http://url.app/api/v4/projects/42/repository/tags",
                params=params,
                headers=headers,
            )
