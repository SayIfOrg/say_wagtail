from django.contrib.auth import get_user_model
from django.core.cache import cache

import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField


UserModel = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = UserModel
        fields = ("id", "first_name", "last_name", "username")
        filter_fields = {
            "id": ["in"],
            "username": ["exact"],
            "first_name": ["icontains"],
            "last_name": ["icontains"],
        }
        interfaces = (graphene.relay.Node,)


class Profile(graphene.ObjectType):
    users = DjangoFilterConnectionField(UserType)


class Linkings(graphene.ObjectType):
    retrieve_user_by_private_fragment = graphene.Field(
        UserType, required=True, the_uuid=graphene.String(required=True)
    )

    def resolve_retrieve_user_by_private_fragment(self, info, the_uuid, **kwargs):
        """
        returns the corresponding id of the user to the uuid
        """
        user_pk = cache.get(the_uuid)
        return UserModel.objects.get(pk=user_pk)


class NewTmpUser(graphene.Mutation):
    class Arguments:
        preferred_username = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(root, info, preferred_username, first_name, last_name):
        temp_user = UserModel.objects.new_temp_user(
            preferred_username=preferred_username,
            first_name=first_name,
            last_name=last_name,
        )
        return NewTmpUser(user=temp_user)


class TempUser(graphene.ObjectType):
    new_temp_user = NewTmpUser.Field(required=True)
