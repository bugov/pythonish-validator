pythonish-validator
===================

.. figure:: https://travis-ci.org/bugov/pythonish-validator.svg?branch=master

Data validation library for Python without complex schemas.
It's how you write Python code:

🐍 Works with Python >= 3.7

.. code:: python

        from re import compile as regex
        from pythonish_validator.common import Validator

        validator = Validator({
            'name': str,
            'age': int,
            'email': regex(r'^\w+@\w+.\w{2,5}$')
            'skills': [str]
        })

        validator.is_valid({
            'name': 'Georgy',
            'age': 29,
            'email': 'bugov@cpan.org'
            'skills': ['Python', 'Perl', 'C']
        })


What can be easier?

Install
-------

.. code:: bash

        pip3 install pythonish-validator

Error messages
--------------

.. code:: python

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

Basic typing module support
---------------------------

Supported types: List, Dict, Optional, Union.

.. code:: python

        from typing import Dict, List, Optional, Union
        from pythonish_validator.common import validate

        schema_example = {
            'name': str,
            'age': Optional[int],  # None if undefined
            'skill': Union[str, List[str]],  # Awful API, but who cares...
            'level_by_skill': Dict[str, str]
        }

        valid_data = {
            'name': 'Georgy',
            'age': None,
            'skill': ['Python', 'ECMA Script'],
            'level_by_skill': {
                'Python': 'senior',
                'ECMA Script': 'middle',
            }
        }

        validator = validate(schema_example, valid_example)

Features
--------

🗣️ Speak the language of Python classes:

.. code:: python

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

🎓 And even custom validation:

.. code:: python

        import re

        from pythonish_validator.common import Validator


        class EmailType:
            @staticmethod
            def __validation_schema__(data):
                if not isinstance(data, str):
                    return False

                if re.match(r'^\w+@\w+.\w{2,5}$', data) is None:
                    return False

                return True


        class User:
            __validation_schema__ = {
                'id': int,
                'name': str,
                'email': EmailType,
            }


        validator = Validator({
            "users": [User]
        })

        validator.is_valid({
            "users": [
                {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
                {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'},
            ]
        })

If you find any mistake – please write to the issue list 🐨 (https://github.com/bugov/pythonish-validator/issues).
