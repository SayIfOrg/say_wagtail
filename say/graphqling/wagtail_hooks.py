from wagtail import hooks

from ..accounting.queries import Linkings, Profile, TempUser
from .mutations import JWTMutation


@hooks.register("register_schema_mutation")
def register_auth_mutation(mutation_mixins):
    mutation_mixins.append(JWTMutation)


@hooks.register("register_schema_query")
def register_profile_queries(query_mixins):
    query_mixins.append(Profile)


@hooks.register("register_schema_query")
def register_linkings_queries(query_mixins):
    query_mixins.append(Linkings)


@hooks.register("register_schema_mutation")
def register_tmp_user_mutation(mutation_mixins):
    mutation_mixins.append(TempUser)
