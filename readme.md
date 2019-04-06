# pythonish-validator

[![Build Status](https://travis-ci.org/bugov/pythonish-validator.svg?branch=master)](https://travis-ci.org/bugov/pythonish-validator)

Data validation library for Python without complex schemas.
It's how you write Python code:

```Python
from pythonish_validator.common import Validator

validator = Validator({
    'name': str,
    'age': int,
    'skills': [str]
})

validator.is_valid({
    'name': 'Georgy',
    'age': 29,
    'skills': ['Python', 'Perl', 'C']
})
```

What can be easier?

# Install

```bash
pip3 install pythonish-validator
```

## Error messages

```Python
from pythonish_validator.common import validate

validator = validate({
    'name': str,
    'age': int,
    'skills': [str]
}, {
    'name': 'Georgy',
    'age': None,
    'skills': ['Python', 'Perl', 42]
})

assert validator.repr_errors() == [
    "{'age'}->NoneType(None)",
    "{'skills'}->[2]->int(42)"
]
```

## Features

🗣️ Speak the language of Python classes:

```Python
from pythonish_validator.common import Validator


class User:
    __validation_schema__ = {
        'id': int,
        'name': str
    }


validator = Validator({
    "users": [User]
})

# valid structure
validator.is_valid({
    "users": [
        {'id': 1, 'name': 'Alice'},
        {'id': 2, 'name': 'Bob'},
    ]
})

# invalid structure
validator.is_valid({
    "users": [
        {'id': '1', 'name': 'Alice'},
        {'id': 2},
    ]
})

assert validator.repr_errors() == [
    "{'users'}->[0]->{'id'}->str('1')",
    "{'users'}->[1]->{'name'}",
]
```

If you find any mistake – please write to the [issue list 🐨](https://github.com/bugov/pythonish-validator/issues).
