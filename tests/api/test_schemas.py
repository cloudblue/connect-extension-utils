from typing import Optional

from connect_extension_utils.api.schemas import (
    NonNullSchema,
    ReferenceSchema,
    clean_empties_from_dict,
)


class MySchema(NonNullSchema):
    other: ReferenceSchema
    file_name: str
    description: Optional[str]


def test_clean_empties_from_dict():
    d = {
        'id': '12',
        'name': None,
        'address': {
            'location': 'Arrecifes',
            'province': None,
            'coord': {
                'lat': 'some',
                'long': None,
            },
        },
    }
    result = clean_empties_from_dict(d)
    assert result == {
        'id': '12',
        'address': {
            'location': 'Arrecifes',
            'coord': {
                'lat': 'some',
            },
        },
    }


def test_feed_create_schema():
    serializer = MySchema(
        other={'id': 'XX'},
        file_name='the file name',
        description=None,
    )
    assert serializer.dict() == {
        'other': {'id': 'XX'},
        'file_name': 'the file name',
    }
