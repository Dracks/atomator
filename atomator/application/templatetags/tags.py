# Standard Library
import json
import os

# Django imports
from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag("version.html", takes_context=False)
def version_tag():
    version_file = os.path.join(settings.BASE_DIR, "version.json")
    if os.path.exists(version_file):
        with open(version_file) as f:
            version = json.loads(f.read())
    else:
        version = {
            "tag": "unknow",
        }
    return version
