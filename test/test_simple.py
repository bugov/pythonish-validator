from pythonish_validator.common import Validator


DATA_SAMPLE = {
    "hero": {
        "name": "R2-D2",
        "friends": [
            {
                "name": "Luke Skywalker",
                "appearsIn": ["NEWHOPE", "EMPIRE", "JEDI"],
                "friends": [
                    {"name": "Han Solo"},
                    {"name": "Leia Organa"},
                    {"name": "C-3PO"},
                    {"name": "R2-D2"}
                ]
            },
            {
                "name": "Han Solo",
                "appearsIn": ["NEWHOPE", "EMPIRE", "JEDI"],
                "friends": [
                    {"name": "Luke Skywalker"},
                    {"name": "Leia Organa"},
                    {"name": "R2-D2"}
                ]
            },
            {
                "name": "Leia Organa",
                "appearsIn": ["NEWHOPE", "EMPIRE", "JEDI"],
                "friends": [
                    {"name": "Luke Skywalker"},
                    {"name": "Han Solo"},
                    {"name": "C-3PO"},
                    {"name": "R2-D2"}
                ]
            }
        ]
    }
}


def test_valid():
    validator = Validator({
        "hero": {
            "name": str,
            "friends": [
                {
                    "name": str,
                    "appearsIn": [str],
                    "friends": [
                        {"name": str}
                    ]
                }
            ]
        }
    })

    assert validator.is_valid(DATA_SAMPLE)


def test_readme_example():
    validator = Validator({
        'name': str,
        'age': int,
        'skills': [str]
    })

    assert validator.is_valid({
        'name': 'Georgy',
        'age': 29,
        'skills': ['Python', 'Perl', 'C']
    })


def test_non_iterable():
    validator = Validator({
        'name': str,
        'age': int,
        'skills': [str]
    })

    assert not validator.is_valid({
        'name': 'Georgy',
        'age': 29,
        'skills': None
    })

    assert not validator.is_valid(None)
