# Django imports
from django.contrib.auth import get_user_model

# Graphene imports
import graphene
from graphene_django.types import DjangoObjectType

from ..utils import autoresolve_field


class MyProfileType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        exclude = ("password", "is_active")

    @staticmethod
    def resolver(parent, info):
        if info.context.user.is_authenticated:
            return info.context.user
        else:
            return None


class Query(graphene.ObjectType):
    my_profile = autoresolve_field(MyProfileType)
