# Standard Library
from functools import wraps

# Graphene imports
import graphene

GQL_ID = graphene.Int


def autoresolve_field(Cls, *args, **kargs):
    return graphene.Field(Cls, resolver=Cls.resolver, *args, **kargs)


def is_logged(func):
    @wraps(func)
    def fn(self, info, *args, **kargs):
        if info.context.user.is_authenticated:
            return func(self, info, *args, **kargs)
        else:
            raise Exception("You should login before")

    return fn
