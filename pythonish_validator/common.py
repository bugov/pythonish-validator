from copy import deepcopy

empty = object()


class Validator:
    def __init__(self, scheme):
        self.scheme = scheme
        self.current_path = []
        self.errors = []

    def __bool__(self):
        return not self.errors

    def _validate_dict(self, data: dict, scheme_node: dict) -> bool:
        if type(data) != dict:
            self.errors.append(deepcopy(self.current_path))
            return False

        data_keys = set(data.keys())
        scheme_keys = set(scheme_node.keys())
        if data_keys != scheme_keys:
            self.errors.append(deepcopy(self.current_path))
            return False

        is_valid = True
        for key, node in scheme_node.items():
            self.current_path.append((dict, key))

            if not self.is_valid(data[key], node):
                is_valid = False

            self.current_path.pop()

        return is_valid

    def _validate_list(self, data: list, scheme_node: list) -> bool:
        if type(data) != list:
            self.errors.append(deepcopy(self.current_path))
            return False

        is_valid = True
        node = scheme_node[0]

        for idx, val in enumerate(data):
            self.current_path.append((list, idx))

            if not self.is_valid(val, node):
                is_valid = False

            self.current_path.pop()

        return is_valid

    def _validate_object(self, data, scheme_node) -> bool:
        self.current_path.append((type(data), data))
        is_valid = True

        if scheme_node is None:
            if data is not None:
                is_valid = False
        elif type(data) != scheme_node:
            is_valid = False

        if not is_valid:
            self.errors.append(deepcopy(self.current_path))

        self.current_path.pop()
        return is_valid

    def is_valid(self, data, scheme_node=empty) -> bool:
        if scheme_node is empty:
            self.current_path = []
            self.errors = []
            scheme_node = self.scheme

        is_valid = True

        if isinstance(scheme_node, dict):
            if not self._validate_dict(data, scheme_node):
                is_valid = False
        elif isinstance(scheme_node, list):
            if not self._validate_list(data, scheme_node):
                is_valid = False
        else:
            if not self._validate_object(data, scheme_node):
                is_valid = False

        return is_valid

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

        return rules


def validate(scheme, data) -> Validator:
    validator = Validator(scheme)
    validator.is_valid(data)
    return validator
