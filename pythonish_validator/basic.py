from copy import deepcopy
from re import Pattern
from typing import _GenericAlias

empty = object()


def is_typing(obj) -> bool:
    return isinstance(obj, _GenericAlias)


def has_custom_validation_schema(obj) -> bool:
    return hasattr(obj, '__validation_schema__')


class CheckChain:
    """
    >>> chain = CheckChain()
    >>> chain \
    ...     .add(lambda x: isinstance(x, dict), validate_dict) \
    ...     .add(lambda x: True, validate_object)
    >>> chain.is_valid(BaseValidator(...), {'age': 30}, {'age': int})
    True
    """
    def __init__(self):
        self.queue = []

    def add(self, grep, validator) -> 'CheckChain':
        self.queue.append((grep, validator))
        return self

    def is_valid(self, context, data, schema_node) -> bool:
        for grep, validator in self.queue:
            if grep(schema_node):
                return validator(context, data, schema_node)

        return False


class BaseValidator:
    """
    >>> chain = CheckChain().add(lambda x: isinstance(x, dict), validate_dict)
    >>> validator = BaseValidator(chain, {'age': int})
    >>> validator.is_valid({'age': 30})
    True
    """
    def __init__(self, chain: CheckChain, schema):
        self.schema = schema
        self.current_path = []
        self.errors = []
        self.check_chain = chain

    def __bool__(self):
        return not self.errors

    def is_valid(self, data, schema_node=empty) -> bool:
        if schema_node is empty:
            self.current_path = []
            self.errors = []
            schema_node = self.schema

        return self.check_chain.is_valid(self, data, schema_node)

    def repr_errors(self) -> list:
        rules = []
        for path in self.errors:
            rule = []
            for klass, data in path:
                if klass == dict:
                    rule.append('{%r}' % data)
                elif klass == list:
                    rule.append('[%r]' % data)
                else:
                    rule.append('%s(%r)' % (klass.__qualname__, data))

            rules.append('->'.join(rule))

        return list(set(rules))


def validate_object(ctx: BaseValidator, obj, schema_node) -> bool:
    """ If the object is an instance of schema_node.
        The last mile for simple (non-composite) types.
    """
    ctx.current_path.append((type(obj), obj))
    is_valid = True

    if schema_node is None:
        if obj is not None:
            is_valid = False
    elif type(obj) != schema_node:
        is_valid = False

    if not is_valid:
        ctx.errors.append(deepcopy(ctx.current_path))

    ctx.current_path.pop()
    return is_valid


def validate_dict(ctx: BaseValidator, data: dict, schema_node: dict) -> bool:
    """ If the object should be dict.
        Check all keys and recursive validate values.
    """
    if type(data) != dict:
        ctx.current_path.append((type(data), data))
        ctx.errors.append(deepcopy(ctx.current_path))
        ctx.current_path.pop()
        return False

    data_keys = set(data.keys())
    schema_keys = set(schema_node.keys())
    if data_keys != schema_keys:
        for key in data_keys ^ schema_keys:
            ctx.current_path.append((dict, key))
            ctx.errors.append(deepcopy(ctx.current_path))
            ctx.current_path.pop()
        return False

    is_valid = True
    for key, node in schema_node.items():
        ctx.current_path.append((dict, key))

        if not ctx.is_valid(data[key], node):
            is_valid = False

        ctx.current_path.pop()

    return is_valid


def validate_typing_dict(ctx: BaseValidator, data: dict, schema_part: _GenericAlias) -> bool:
    schema_part = schema_part.__args__
    if type(data) != dict:
        ctx.current_path.append((type(data), data))
        ctx.errors.append(deepcopy(ctx.current_path))
        ctx.current_path.pop()
        return False

    is_valid = True

    schema_key, schema_val = schema_part
    for key in data.keys():
        if not isinstance(key, schema_key):
            is_valid = False
            ctx.current_path.append((dict, key))
            ctx.errors.append(deepcopy(ctx.current_path))
            ctx.current_path.pop()

    for key, val in data.items():
        ctx.current_path.append((dict, key))

        if not ctx.is_valid(data[key], schema_val):
            is_valid = False

        ctx.current_path.pop()

    return is_valid


def validate_list(ctx: BaseValidator, data: list, schema_node: list) -> bool:
    if type(data) != list:
        ctx.current_path.append((type(data), data))
        ctx.errors.append(deepcopy(ctx.current_path))
        ctx.current_path.pop()
        return False

    is_valid = True
    node = schema_node[0]

    for idx, val in enumerate(data):
        ctx.current_path.append((list, idx))

        if not ctx.is_valid(val, node):
            is_valid = False

        ctx.current_path.pop()

    return is_valid


def validate_typing_list(ctx: BaseValidator, data: dict, schema_part: _GenericAlias) -> bool:
    return validate_list(ctx, data, list(schema_part.__args__))


def validate_optional(ctx: BaseValidator, data, schema_node) -> bool:
    is_valid = True

    matched = [
        klass for klass in schema_node.__args__
            if is_typing(klass)
                or isinstance(data, klass)
                or has_custom_validation_schema(klass)
    ]

    tmp_error = deepcopy(ctx.errors)
    tmp_path = deepcopy(ctx.current_path)
    if not any([ctx.is_valid(data, a) for a in matched]):
        ctx.current_path.append((type(data), data))
        ctx.errors.append(deepcopy(ctx.current_path))
        ctx.current_path.pop()
        is_valid = False
    else:
        ctx.current_path = tmp_path
        ctx.errors = tmp_error

    return is_valid


def validate_validation_schema(ctx: BaseValidator, data, schema_node) -> bool:
    is_valid = True

    validation_schema = getattr(schema_node, '__validation_schema__')
    if hasattr(validation_schema, '__call__'):
        if not validation_schema(data):
            ctx.current_path.append((type(data), data))
            ctx.errors.append(deepcopy(ctx.current_path))
            ctx.current_path.pop()
            is_valid = False
    else:
        if not ctx.is_valid(data, schema_node.__validation_schema__):
            is_valid = False

    return is_valid


def validate_regex(ctx: BaseValidator, data: str, schema_node: Pattern) -> bool:
    if (
        not isinstance(data, str)
        or schema_node.match(data) is None
    ):
        ctx.current_path.append((type(data), data))
        ctx.errors.append(deepcopy(ctx.current_path))
        ctx.current_path.pop()
        return False

    return True
