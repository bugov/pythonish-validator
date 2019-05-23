from copy import deepcopy
from typing import Union, _GenericAlias

empty = object()


def _is_typing(obj):
    return isinstance(obj, _GenericAlias)


class Validator:
    def __init__(self, schema):
        self.schema = schema
        self.current_path = []
        self.errors = []

    def __bool__(self):
        return not self.errors

    def _validate_dict(self, data: dict, schema_node: dict) -> bool:
        if type(data) != dict:
            self.current_path.append((type(data), data))
            self.errors.append(deepcopy(self.current_path))
            self.current_path.pop()
            return False

        data_keys = set(data.keys())
        schema_keys = set(schema_node.keys())
        if data_keys != schema_keys:
            for key in data_keys ^ schema_keys:
                self.current_path.append((dict, key))
                self.errors.append(deepcopy(self.current_path))
                self.current_path.pop()
            return False

        is_valid = True
        for key, node in schema_node.items():
            self.current_path.append((dict, key))

            if not self.is_valid(data[key], node):
                is_valid = False

            self.current_path.pop()

        return is_valid

    def _validate_typing_dict(self, data: dict, schema_part: tuple):
        if type(data) != dict:
            self.current_path.append((type(data), data))
            self.errors.append(deepcopy(self.current_path))
            self.current_path.pop()
            return False

        is_valid = True

        schema_key, schema_val = schema_part
        for key in data.keys():
            if not isinstance(key, schema_key):
                is_valid = False
                self.current_path.append((dict, key))
                self.errors.append(deepcopy(self.current_path))
                self.current_path.pop()

        for key, val in data.items():
            self.current_path.append((dict, key))

            if not self.is_valid(data[key], schema_val):
                is_valid = False

            self.current_path.pop()

        return is_valid

    def _validate_list(self, data: list, schema_node: list) -> bool:
        if type(data) != list:
            self.current_path.append((type(data), data))
            self.errors.append(deepcopy(self.current_path))
            self.current_path.pop()
            return False

        is_valid = True
        node = schema_node[0]

        for idx, val in enumerate(data):
            self.current_path.append((list, idx))

            if not self.is_valid(val, node):
                is_valid = False

            self.current_path.pop()

        return is_valid

    def _validate_object(self, data, schema_node) -> bool:
        self.current_path.append((type(data), data))
        is_valid = True

        if schema_node is None:
            if data is not None:
                is_valid = False
        elif type(data) != schema_node:
            is_valid = False

        if not is_valid:
            self.errors.append(deepcopy(self.current_path))

        self.current_path.pop()
        return is_valid

    def _validate__validation_schema__(self, data, schema_node) -> bool:
        is_valid = True

        validation_schema = getattr(schema_node, '__validation_schema__')
        if hasattr(validation_schema, '__call__'):
            if not validation_schema(data):
                self.current_path.append((type(data), data))
                self.errors.append(deepcopy(self.current_path))
                self.current_path.pop()
                is_valid = False
        else:
            if not self.is_valid(data, schema_node.__validation_schema__):
                is_valid = False

        return is_valid

    def _validate_optional(self, data, schema_node) -> bool:
        is_valid = True

        matched = [
            klass for klass in schema_node.__args__
            if _is_typing(klass) or isinstance(data, klass)
        ]

        tmp_error = deepcopy(self.errors)
        tmp_path = deepcopy(self.current_path)
        if not any([self.is_valid(data, a) for a in matched]):
            self.current_path.append((type(data), data))
            self.errors.append(deepcopy(self.current_path))
            self.current_path.pop()
            is_valid = False
        else:
            self.current_path = tmp_path
            self.errors = tmp_error

        return is_valid

    def is_valid(self, data, schema_node=empty) -> bool:
        if schema_node is empty:
            self.current_path = []
            self.errors = []
            schema_node = self.schema

        if isinstance(schema_node, dict):
            return self._validate_dict(data, schema_node)

        if isinstance(schema_node, list):
            return self._validate_list(data, schema_node)

        if _is_typing(schema_node):
            if schema_node.__origin__ is Union:
                return self._validate_optional(data, schema_node)
            if schema_node.__origin__ is list:
                return self._validate_list(data, list(schema_node.__args__))
            if schema_node.__origin__ is dict:
                return self._validate_typing_dict(data, schema_node.__args__)

        if hasattr(schema_node, '__validation_schema__'):
            return self._validate__validation_schema__(data, schema_node)

        return self._validate_object(data, schema_node)

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


def validate(schema, data) -> Validator:
    validator = Validator(schema)
    validator.is_valid(data)
    return validator
