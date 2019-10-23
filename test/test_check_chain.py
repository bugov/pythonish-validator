from pythonish_validator.basic import CheckChain


def test_empty_pipeline():
    pipe = CheckChain()
    assert not pipe.is_valid(None, 42, int)
