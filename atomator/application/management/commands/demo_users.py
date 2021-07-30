# Standard Library
import logging

# Django imports
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand


class Command(BaseCommand):
    """
    Check data validity in the database ::
        manage.py data_validator
    """

    def handle(self, *args, **options):
        User = get_user_model()
        admin = User.objects.create(
            username="admin", is_staff=True, is_active=True, is_superuser=True
        )
        admin.set_password("admin")
        admin.save()
