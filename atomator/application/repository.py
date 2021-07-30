# Standard Library
import logging

# Other libraries
import requests

logger = logging.getLogger()


def extract_config(hash_data, obj):
    for int_value in obj.extra_int_set.all():
        hash_data[int_value.key] = int_value.value
    for sting_value in obj.extra_string_set.all():
        hash_data[sting_value.key] = sting_value.value
    for text_value in obj.extra_text_set.all():
        hash_data[sting_value.key] = text_value.value


class GitlabRepository:
    def __init__(self, application, repository):
        hash_data = {}
        repo_app = application.repository_set.through.objects.get(
            application=application, repository=repository
        )
        extract_config(hash_data, repository)
        extract_config(hash_data, repo_app)
        self.url = repository.url
        self.token = hash_data["token"]
        self.project_id = hash_data["project_id"]

    def create_tag(self, tag, hsh):
        headers = {"PRIVATE-TOKEN": self.token}
        # tag_name
        # ref
        params = {"tag_name": tag, "ref": hsh}
        response = requests.post(
            f"{self.url}/api/v4/projects/{self.project_id}/repository/tags",
            params=params,
            headers=headers,
        )
        if response.status_code != 201:
            logging.error(
                f"Creation of tag {tag} for {self.project_id} in {self.url} failed with code {response.status_code}"
            )
