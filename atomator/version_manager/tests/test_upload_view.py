# Django imports
from django.test import TestCase

# Atom platform
from atomator.application.models import Application

from ..models import Build, ChangesChoices
from ..views import UploadView


class TestUploadViewClass(TestCase):
    def setUp(self):
        self.app = Application.objects.create(name="Application")

        self.subject = UploadView()

    def tearDown(self):
        Build.objects.all().delete()
        Application.objects.all().delete()

    def test_new_version(self):
        update = self.subject.new_version("default patch", 0, 0, 0)
        self.assertEqual(update, (0, 0, 1, ChangesChoices.patch))

        update = self.subject.new_version("something \n [minor] fuck minor", 0, 0, 3)
        self.assertEqual(update, (0, 1, 0, ChangesChoices.minor))

        update = self.subject.new_version("[MaJoR] default patch", 2, 1, 3)
        self.assertEqual(update, (3, 0, 0, ChangesChoices.major))

    def test_generate_new_version_without_previous(self):
        build = self.subject.generate_version(
            self.app, "[Minor] other", "develop", "Some hash"
        )

        self.assertEqual(build.major, 0)
        self.assertEqual(build.minor, 1)
        self.assertEqual(build.patch, 0)
        self.assertEqual(build.branch, "develop")
        self.assertEqual(build.change, ChangesChoices.minor)

    def test_generate_new_version_without_release_but_with_draft(self):
        Build.objects.create(
            application=self.app,
            major=0,
            minor=1,
            patch=0,
            commit="...",
            change=ChangesChoices.minor,
        )

        build = self.subject.generate_version(
            self.app, "default without anything", "main", "**"
        )

        self.assertEqual(build.major, 0)
        self.assertEqual(build.minor, 1)
        self.assertEqual(build.patch, 0)
        self.assertEqual(build.change, ChangesChoices.minor)
        self.assertEqual(build.commit, "**")

    def test_generate_new_version_ignoring_other_branches(self):
        Build.objects.create(
            application=self.app,
            major=1,
            minor=0,
            patch=0,
            branch="develop",
            commit="...",
            change=ChangesChoices.major,
        )

        Build.objects.create(
            application=self.app,
            major=0,
            minor=0,
            patch=1,
            release=True,
            commit="...123",
            change=ChangesChoices.patch,
        )

        build = self.subject.generate_version(
            self.app, "[minor] bla bla bla", "main", "**"
        )

        self.assertEqual(build.major, 0)
        self.assertEqual(build.minor, 1)
        self.assertEqual(build.patch, 0)
        self.assertEqual(build.change, ChangesChoices.minor)
        self.assertEqual(build.commit, "**")

    def _test_generate_new_version_without_release(self):
        Build.objects.create(
            application=self.app,
            major=0,
            minor=1,
            patch=0,
            commit="...",
            change=ChangesChoices.minor,
        )

        build = self.subject.generate_version(
            self.app, "[major] default without anything", "**"
        )

        self.assertEqual(build.major, 1)
        self.assertEqual(build.minor, 0)
        self.assertEqual(build.patch, 0)
        self.assertEqual(build.change, ChangesChoices.major)
        self.assertEqual(build.commit, "**")

    def test_generate_new_version_same_change(self):
        Build.objects.create(
            application=self.app,
            major=0,
            minor=1,
            patch=0,
            commit="...",
            change=ChangesChoices.minor,
        )

        build = self.subject.generate_version(
            self.app, "[minor]default without anything", "main", "**"
        )

        self.assertEqual(build.major, 0)
        self.assertEqual(build.minor, 1)
        self.assertEqual(build.patch, 0)
        self.assertEqual(build.change, ChangesChoices.minor)
        self.assertEqual(build.commit, "**")
