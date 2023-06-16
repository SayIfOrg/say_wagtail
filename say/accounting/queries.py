from django.core.cache import cache

import graphene


class Linkings(graphene.ObjectType):
    retrieve_user_by_private_fragment = graphene.Int(
        required=True, the_uuid=graphene.String(required=True)
    )

    def resolve_retrieve_user_by_private_fragment(self, info, the_uuid, **kwargs):
        """
        returns the corresponding id of the user to the uuid
        """
        user_pk = cache.get(the_uuid)
        return user_pk
