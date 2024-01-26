from connect.client import ConnectClient
from connect.client.rql import R
from connect_extension_utils.connect_services.base import (
    get_extension_owner_client,
    get_extension_owner_installation,
)


def test_get_client_owner(logger):
    client = get_extension_owner_client(logger)
    assert isinstance(client, ConnectClient)
    assert client.api_key == "ApiKey fake"
    assert client.endpoint == "https://api.test.wow/public/v1"


def test_get_extension_owner_installation(connect_client, client_mocker_factory):
    client_mocker = client_mocker_factory(base_url=connect_client.endpoint)

    rql = R().environment.id.eq("ENV-123")
    (
        client_mocker.ns("devops")
        .installations.filter(rql)
        .limit(1)
        .mock(
            return_value=[{"id": "INS-123"}],
        )
    )
    installation = get_extension_owner_installation(connect_client)
    assert installation == {"id": "INS-123"}
