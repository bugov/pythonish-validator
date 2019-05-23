from pythonish_validator.common import validate, Validator


def test_repr_one():
    validator = Validator(str)

    validator.is_valid("asd")
    validator.is_valid([1])
    assert validator.repr_errors() == ["[[1]]"]

    validator = validate({
        'name': str,
        'age': int,
        'skills': [str]
    }, {
        'name': 'Georgy',
        'age': None,
        'skills': ['Python', 'Perl', 'C']
    })
    assert validator.repr_errors() == ["{'age'}->NoneType(None)"]


def test_repr_may():
    validator = validate({
        'name': str,
        'age': int,
        'skills': [str]
    }, {
        'name': 'Georgy',
        'age': None,
        'skills': ['Python', 'Perl', 42]
    })
    assert set(validator.repr_errors()) == {
        "{'age'}->NoneType(None)",
        "{'skills'}->[2]->int(42)",
    }
