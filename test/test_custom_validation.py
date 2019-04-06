import re

from pythonish_validator.common import Validator


DATA_SAMPLE = {
    "users": [
        {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
        {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'},
    ]
}
WRONG_DATA_SAMPLE = {
    "users": [
        {'id': '1', 'name': 'Alice', 'email': 'hello'},
        {'id': 2, 'email': 'bob@example.com'},
    ]
}


class EmailType:
    @staticmethod
    def __validation_schema__(data):
        if not isinstance(data, str):
            return False

        if re.match(r'\w+@\w+.\w{2,5}', data) is None:
            return False

        return True


class User:
    __validation_schema__ = {
        'id': int,
        'name': str,
        'email': EmailType,
    }


def test_object():
    validator = Validator({
        "users": [User]
    })

    assert validator.is_valid(DATA_SAMPLE)

    assert not validator.is_valid(WRONG_DATA_SAMPLE)
    assert set(validator.repr_errors()) == {
        "{'users'}->[0]->{'id'}->str('1')",
        "{'users'}->[1]->{'name'}",
        "{'users'}->[0]->{'email'}->str('hello')",
    }
