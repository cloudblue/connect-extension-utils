import json

import pytest

from connect.client import ClientError
from connect.eaas.core.utils import client_error_exception_handler
from connect_extension_utils.api.errors import ExtensionErrorBase, Http404


class MyError(ExtensionErrorBase):
    PREFIX = 'BAD'

    ERRORS = {
        0: "Some error.",
        1: "Error with param: {param}.",
        3: "",
    }


def test_extension_error():
    error = MyError.BAD_000()
    assert isinstance(error, ClientError)
    assert error.status_code == 400

    json_error = client_error_exception_handler(None, error).body.decode()

    assert json_error == '{"error_code":"BAD_000","errors":["Some error."]}'


def test_error_with_param():
    error = MyError.BAD_001(format_kwargs={'param': 'Foo'})
    assert isinstance(error, ClientError)
    assert error.status_code == 400

    json_error = client_error_exception_handler(None, error).body.decode()

    assert json_error == '{"error_code":"BAD_001","errors":["Error with param: Foo."]}'


@pytest.mark.parametrize(
    'errors,expected',
    (('Error', 'Error'), (None, 'Unexpected error.')),
)
def test_default_error_message(errors, expected):
    error = MyError.BAD_003(errors=errors)
    assert isinstance(error, ClientError)
    assert error.status_code == 400

    json_error = client_error_exception_handler(None, error).body.decode()

    assert json.loads(json_error) == {"error_code": "BAD_003", "errors": [f'{expected}']}


def test_404_not_found_error():
    not_found = Http404('EXT-123')

    assert isinstance(not_found, ClientError)
    assert not_found.status_code == 404

    json_error = client_error_exception_handler(None, not_found).body.decode()

    assert json_error == '{"error_code":"NFND_000","errors":["Object `EXT-123` not found."]}'
