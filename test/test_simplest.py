from pythonish_validator.common import Validator


def test_str():
    validator = Validator(str)
    assert validator.is_valid('hello')
    assert not validator.is_valid(1)


def test_none():
    validator = Validator(None)
    assert validator.is_valid(None)
    assert not validator.is_valid('')


def test_int():
    validator = Validator(int)
    assert validator.is_valid(1)
    assert not validator.is_valid('1')


def test_float():
    validator = Validator(float)
    assert validator.is_valid(1.123)
    assert not validator.is_valid(True)


def test_bool():
    validator = Validator(bool)
    assert validator.is_valid(True)
    assert not validator.is_valid(None)


def test_list():
    validator = Validator(list)
    assert validator.is_valid([1, 2, 3])
    assert not validator.is_valid('qwe')


def test_dict():
    validator = Validator(dict)
    assert validator.is_valid({'year': 2019})
    assert not validator.is_valid([1, 2, 3])
