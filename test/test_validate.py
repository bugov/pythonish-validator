from pythonish_validator.common import validate


def test_validate():
    assert validate({
        'name': str,
        'age': int,
        'skills': [str]
    }, {
        'name': 'Georgy',
        'age': 29,
        'skills': ['Python', 'Perl', 'C']
    })


def test_validate_failed():
    validator = validate({
        'name': str,
        'age': int,
        'skills': [str]
    }, {
        'name': 'Georgy',
        'age': None,
        'skills': ['Python', 'Perl', 'C']
    })

    assert not validator
