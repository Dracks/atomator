# Django imports
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

# Graphene imports
import graphene

from ..utils import autoresolve_field
from .query import MyProfileType


class LoginErrorType(graphene.ObjectType):
    code = graphene.Int(required=True)
    message = graphene.String(required=True)


class Login(graphene.Mutation):
    profile = graphene.Field(MyProfileType)
    error = graphene.Field(LoginErrorType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    @staticmethod
    def mutate(parent, info, **kwargs):
        credentials = {
            "username": kwargs.get("username"),
            "password": kwargs.get("password"),
        }
        user = authenticate(info.context, **credentials)
        if user and user.is_active:
            auth_login(info.context, user)
            return Login(profile=user)
        else:
            error = {"code": 1, "message": "Not valid user or password"}
            return Login(error=error)


class Logout(graphene.Mutation):
    status = graphene.String()

    @staticmethod
    def mutate(parent, info):
        status = "Already not logged"
        if info.context.user.is_authenticated:
            auth_logout(info.context)
            status = "Done"
        return Logout(status=status)


class Session(graphene.ObjectType):
    login = Login.Field()
    logout = Logout.Field()

    @staticmethod
    def resolver(parent, info):
        return Session()


class Mutation(graphene.ObjectType):
    session = autoresolve_field(Session)
