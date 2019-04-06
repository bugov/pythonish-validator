from pythonish_validator.common import validate


def test_validate():
    assert not validate({
        'name': str,
        'age': int,
        'skills': [str]
    }, {
        'name': 'Georgy',
    })
