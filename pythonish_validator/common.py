from functools import partial
from re import Pattern
from typing import Union, _GenericAlias

from pythonish_validator.basic import (
    empty,  # noqa
    is_typing,
    has_custom_validation_schema,
    CheckChain,
    BaseValidator,
    validate_dict,
    validate_list,
    validate_object,
    validate_optional,
    validate_regex,
    validate_typing_dict,
    validate_typing_list,
    validate_validation_schema,
)


_common_check_chain = (
    CheckChain()
    .add(lambda x: isinstance(x, dict), validate_dict)
    .add(lambda x: isinstance(x, list), validate_list)
    .add(lambda x: is_typing(x) and x.__origin__ is Union, validate_optional)
    .add(lambda x: is_typing(x) and x.__origin__ is list, validate_typing_list)
    .add(lambda x: is_typing(x) and x.__origin__ is dict, validate_typing_dict)
    .add(lambda x: has_custom_validation_schema(x), validate_validation_schema)
    .add(lambda x: isinstance(x, Pattern), validate_regex)
    .add(lambda x: True, validate_object)  # Last check
)

Validator = partial(BaseValidator, _common_check_chain)


def validate(schema, data) -> Validator:
    validator = Validator(schema)
    validator.is_valid(data)
    return validator
