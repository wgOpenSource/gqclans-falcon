import graphene


class DefaultQuery(graphene.ObjectType):
    ping = graphene.String(description='A basic GraphQL object.')

    def resolve_ping(self, info):
        return 'ok'


default_schema = graphene.Schema(query=DefaultQuery)
