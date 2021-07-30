# Standard Library
import json

# Other libraries
import graphene
from graphene_django.utils.testing import GraphQLTestCase


def graphQlTest(**kwargs):
    def decorator(cls):
        class NewCls(cls):
            GRAPHQL_SCHEMA = graphene.Schema(**kwargs)

            def assertResponseNoErrors(self, response):
                try:
                    content = json.loads(response.content)
                    if "errors" in content.keys():
                        print(json.dumps(content, indent=4))
                        super(NewCls, self).assertResponseNoErrors(response)
                    return content
                except json.decoder.JSONDecodeError:
                    super(NewCls, self).assertResponseNoErrors(response)

        return NewCls

    return decorator


def get_query_response(**kwargs):
    return {"data": kwargs}
