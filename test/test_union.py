from typing import Optional, List, Union
from pythonish_validator.common import Validator


def test_optional_str():
    validator = Validator(Optional[str])

    validator.is_valid(None)
    validator.is_valid("asd")
    validator.is_valid([1])
    assert validator.repr_errors() == ["[[1]]"]


    validator = Validator({
        'name': str,
        'age': int,
        'selected_skill': Optional[str]
    })

    assert validator.is_valid({
        'name': 'Georgy',
        'age': 29,
        'selected_skill': 'Python'
    }), validator.repr_errors()

    assert validator.is_valid({
        'name': 'Georgy',
        'age': 29,
        'selected_skill': None
    }), validator.repr_errors()

    validator.is_valid({
        'name': 'Georgy',
        'age': 29,
        'selected_skill': 1
    })
    assert validator.repr_errors() == ["{'selected_skill'}->int(1)"]


def test_optional_list():
    validator = Validator({
        'selected_skills': Optional[List[str]]
    })

    assert validator.is_valid({
        'selected_skills': ['Python']
    }), validator.repr_errors()

    assert validator.is_valid({
        'selected_skills': None
    }), validator.repr_errors()

    validator.is_valid({
        'selected_skills': 'Python'
    })

    assert validator.repr_errors() == ["{'selected_skills'}->str('Python')"]


def test_union_str():
    validator = Validator(Union[int, str])
    assert validator.is_valid(1), validator.repr_errors()
    assert validator.is_valid("1"), validator.repr_errors()

    validator.is_valid([1])
    assert validator.repr_errors() == ['[[1]]']


def test_union_complex():
    validator = Validator({
        'value': Union[Optional[int], List[str]]
    })
    assert validator.is_valid({'value': None}), validator.repr_errors()
    assert validator.is_valid({'value': 1}), validator.repr_errors()
    assert validator.is_valid({'value': ['1']}), validator.repr_errors()
