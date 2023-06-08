from wagtail import hooks

from .mutations import JWTMutation


@hooks.register("register_schema_mutation")
def register_author_mutation(mutation_mixins):
    mutation_mixins.append(JWTMutation)
