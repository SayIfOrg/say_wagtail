import collections

from django.core.exceptions import ValidationError

import pydantic


def pydantic_validation_err_to_djs(error: pydantic.ValidationError) -> ValidationError:
    message = collections.defaultdict[str, list[ValidationError]](list)
    for err in error.errors():
        for field_name in err["loc"]:
            message[field_name].append(
                ValidationError(message=err["msg"], code=err["type"])
            )
    return ValidationError(message=message)
