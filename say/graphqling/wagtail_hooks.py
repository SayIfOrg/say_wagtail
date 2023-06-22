from wagtail import hooks

from ..accounting.queries import Linkings, TempUser
from .mutations import JWTMutation


@hooks.register("register_schema_mutation")
def register_author_mutation(mutation_mixins):
    mutation_mixins.append(JWTMutation)


@hooks.register("register_schema_query")
def register_linkings_queries(query_mixins):
    query_mixins.append(Linkings)


@hooks.register("register_schema_mutation")
def register_tmp_user_mutation(mutation_mixins):
    mutation_mixins.append(TempUser)
