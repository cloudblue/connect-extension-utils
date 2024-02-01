import pytest

from connect.client import ClientError
from connect_extension_utils.api.views import get_object_or_404, get_user_data_from_auth_token


def test_get_user_data_from_auth_token(connect_auth_header):
    result = get_user_data_from_auth_token(connect_auth_header)

    assert result == {'id': 'SU-295-689-628', 'name': 'Neri'}


def test_get_object_or_404_success(dbsession, my_model_factory):
    obj = my_model_factory()

    obj_from_db = get_object_or_404(
        dbsession,
        my_model_factory._meta.model,
        (my_model_factory._meta.model.id == obj.id,),
        obj.id,
    )

    assert obj_from_db == obj


def test_get_object_or_404_not_found(dbsession, my_model_factory):
    with pytest.raises(ClientError) as ex:
        get_object_or_404(
            dbsession,
            my_model_factory._meta.model,
            (my_model_factory._meta.model.id == '000',),
            '000',
        )
    assert ex.value.error_code == 'NFND_000'
    assert ex.value.message == 'Object `000` not found.'
