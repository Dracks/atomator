# Django imports
from django.urls import path

from .views import UploadView, download_view, metadata_view

urlpatterns = [
    path(
        "upload_version/<app_token>", UploadView.as_view(), name="upload_file_version"
    ),
    # path("metadata/<app_token>/latest", metadata_view, name="metadata-latest"),
    # path("metadata/<app_token>/<int:version_id>", metadata_view, name="metadata"),
    path("download/version/<file_id>", download_view, name="download-version"),
]
