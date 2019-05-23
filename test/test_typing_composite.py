from typing import List, Dict, Optional

from pythonish_validator.common import Validator


def test_list():
    validator = Validator(List[str])

    assert validator.is_valid(["asd"]), validator.repr_errors()
    assert validator.is_valid([]), validator.repr_errors()

    validator.is_valid([1])
    assert validator.repr_errors() == ["[0]->int(1)"]

    validator = Validator(List[List[str]])
    assert validator.is_valid([["zxc"], ["qwe"], ["asd"], []]), validator.repr_errors()

    validator = Validator(List[List[Optional[str]]])
    assert validator.is_valid([[None], ["qwe"], ["asd"], []]), validator.repr_errors()


def test_dict():
    validator = Validator(Dict[str, int])

    assert validator.is_valid({"a": 1}), validator.repr_errors()
    assert validator.is_valid({}), validator.repr_errors()

    validator.is_valid({1: 1})
    assert validator.repr_errors() == ['{1}']

    validator.is_valid({"a": "a"})
    assert validator.repr_errors()  == ["{'a'}->str('a')"]

    validator.is_valid(1)
    assert validator.repr_errors()  == ["int(1)"]
