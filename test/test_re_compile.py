import re

from pythonish_validator.common import Validator


def test_simple_match():
    validator = Validator(re.compile(r'^https?://'))
    assert validator.is_valid('https://900913.ru')
    assert Validator(re.compile(r'^https?://')).is_valid('http://google.com')

    assert not Validator(re.compile(r'^https?://')).is_valid('    http://google.com')
    assert not Validator(re.compile(r'^https?://')).is_valid('900913.ru')


def test_composite():
    validator = Validator({
        'name': str,
        'email': re.compile(r'^[\w_\-.+]+@[\w\-.+]+.\w+'),
        'blog': re.compile(r'^https?://[\w\-.+]+.\w+'),
    })

    assert validator.is_valid({
        'name': 'Georgy',
        'email': 'bugov@cpan.org',
        'blog': 'https://900913.ru'
    })

    assert not validator.is_valid({
        'name': 'Georgy',
        'email': 'bugov[at]cpan.org',
        'blog': '900913.ru'
    })
    assert set(validator.repr_errors()) == {
        "{'email'}->str('bugov[at]cpan.org')",
        "{'blog'}->str('900913.ru')",
    }

    validator = Validator({
        'media': {
            'web': [
                re.compile(r'^https?://[\w\-.+]+.\w+')
            ]
        }
    })
    assert validator.is_valid({
        'media': {
            'web': ['https://900913.ru']
        }
    })

    assert not validator.is_valid({
        'media': {
            'web': ['https://900913.ru', '900913.net']
        }
    })
    assert validator.repr_errors() == ["{'media'}->{'web'}->[1]->str('900913.net')"]
