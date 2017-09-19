import pytest

from warlok.parser import (
    get_message_template,
    parse_message_into_fields,
    DuplicatedFieldMessage
)


def test_get_message_template_empty():
    result = get_message_template({'title': '', 'summary': '', 'reviewers': ''})

    expected = """

Summary:


Reviewers:
"""

    assert result == expected


def test_get_message_template_values():
    result = get_message_template({
        'title': 'title',
        'summary': 'this is summary',
        'reviewers': 'john, joe'
    })

    expected = """title

Summary: this is summary


Reviewers: john, joe
"""

    assert result == expected


def test_parse_message_info_fields_empty():
    result = parse_message_into_fields("", ['title', 'summary'])

    expected = {
        'title': '',
        'summary': '',
    }
    assert result == expected


def test_parse_message_info_fields_title_implicit():
    result = parse_message_into_fields(
        "This is title",
        ['title', 'summary']
    )

    expected = {
        'title': 'This is title',
        'summary': '',
    }
    assert result == expected


def test_parse_message_info_fields_title_explicit():
    result = parse_message_into_fields(
        "Title: This is title",
        ['title', 'summary']
    )

    expected = {
        'title': 'This is title',
        'summary': '',
    }
    assert result == expected


def test_parse_message_info_fields_title_all():
    result = parse_message_into_fields(
        """Title: This is title

Summary: This is
a
multi
line



summary.
""",
        ['title', 'summary']
    )

    expected = {
        'title': 'This is title',
        'summary': 'This is\na\nmulti\nline\n\n\n\nsummary.',
    }
    assert result == expected


def test_parse_message_info_fields_title_unknown():
    result = parse_message_into_fields(
        """Title: This is title

Summary: This is summary.

Reviewers: john, jane
""",
        ['title', 'summary']
    )

    expected = {
        'title': 'This is title',
        'summary': 'This is summary.\n\nReviewers: john, jane',
    }
    assert result == expected


def test_parse_message_info_fields_title_duplicate():
    with pytest.raises(ValueError) as err:
        parse_message_into_fields(
            """Title: This is title

Summary: This is summary.
Summary: Another summary.
""",
            ['title', 'summary']
        )

    assert str(err.value) == DuplicatedFieldMessage(field="Summary")
