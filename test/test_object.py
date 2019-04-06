from pythonish_validator.common import Validator


DATA_SAMPLE = {
    "users": [
        {'id': 1, 'name': 'Alice'},
        {'id': 2, 'name': 'Bob'},
    ]
}
WRONG_DATA_SAMPLE = {
    "users": [
        {'id': '1', 'name': 'Alice'},
        {'id': 2},
        {'id': 3, 'name': 1},
    ]
}


class User:
    __validation_schema__ = {
        'id': int,
        'name': str
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
        "{'users'}->[2]->{'name'}->int(1)",
    }
