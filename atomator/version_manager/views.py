# Standard Library
import json
import os
import re

# Django imports
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

# Atom platform
from atomator.application.models import Token

from .models import Build, Change, ChangesChoices, FileInfo


def write_file(upload_file):
    file_name_data = os.path.splitext(upload_file.name)
    name = default_storage.get_alternative_name(*file_name_data)
    with default_storage.open(name, mode="wb+") as destination:
        for chunk in upload_file.chunks():
            destination.write(chunk)
    return name


class UploadView(View):
    tag_match = re.compile(r"\[([a-zA-Z]*)\]")

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(UploadView, self).dispatch(request, *args, **kwargs)

    def new_version(self, message, major, minor, patch):
        match = self.tag_match.search(message)
        if match:
            label = match.group(1)
            if label.lower() == "major":
                return major + 1, 0, 0, ChangesChoices.major
            if label.lower() == "minor":
                return major, minor + 1, 0, ChangesChoices.minor

        return major, minor, patch + 1, ChangesChoices.patch

    def generate_version(self, app, message, branch, hash):
        prev_release = Build.objects.filter(application=app, release=True).first()
        prev_build = Build.objects.filter(
            application=app, branch=branch, release=False
        ).first()
        if not prev_release:
            prev_release = Build(major=0, minor=0, patch=0)
        if not prev_build:
            prev_build = Build(major=0, minor=0, patch=0, change=ChangesChoices.patch)

        major, minor, patch, change = self.new_version(
            message, prev_release.major, prev_release.minor, prev_release.patch
        )
        if change > prev_build.change:
            major = prev_build.major
            minor = prev_build.minor
            patch = prev_build.patch
            change = prev_build.change

        return Build.objects.create(
            application=app,
            major=major,
            minor=minor,
            patch=patch,
            branch=branch,
            commit=hash,
            change=change,
        )

    def save_file(self, build, upload_file):

        name = upload_file.name
        size = upload_file.size
        content_type = upload_file.content_type
        file_name = write_file(upload_file)

        return FileInfo.objects.create(
            build=build,
            name=name,
            file_name=file_name,
            size=size,
            content_type=content_type,
        )

    def add_changes(self, build, message):
        Change.objects.create(
            build=build, type=Change.ChangeType.UNKNOWN, description=message
        )

    def post(self, request, app_token):
        app = Token.objects.get(token=app_token).application
        if app:
            message = request.POST.get("message")
            hsh = request.POST.get("hash")
            upload_file = request.FILES.get("file")
            branch = request.POST.get("branch", app.release_branch)
            build = self.generate_version(app, message, branch, hsh)
            self.add_changes(build, message)
            self.save_file(build, upload_file)

            return HttpResponse("Upload")


def metadata_view(request, app_token, version_id=None):
    app = Token.objects.get(token=app_token).application
    if app:
        query = Build.objects.filter(application=app)
        if version_id:
            build = query.get(id=version_id)
        else:
            build = query.first()

        return HttpResponse(
            json.dumps(
                {
                    "name": app.name,
                    "major": build.major,
                    "minor": build.minor,
                    "patch": build.patch,
                    "date": build.date.isoformat(),
                    "file": build.file.id,
                    "release": build.release,
                }
            )
        )


def download_view(request, file_id):
    if request.method == "GET":
        file_info = FileInfo.objects.get(uuid=file_id)
        with default_storage.open(file_info.file_name, "rb") as fh:
            response = HttpResponse(fh.read(), content_type=file_info.content_type)
            response["Content-Disposition"] = "inline; filename=" + file_info.name
            return response
