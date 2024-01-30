# -*- coding: utf-8 -*-
#
# Copyright (c) 2024, Imgram Migro
# All rights reserved.
#
import os
from unittest import mock

import pytest
from pytest_factoryboy import register

from connect.client import ConnectClient
from connect_extension_utils.testing.fixtures import *  # noqa: F401 F403
from tests.testing.factories import MyModelFactory, RelatedModelFactory, TransactionalModelFactory


@pytest.fixture
def connect_client():
    return ConnectClient(
        "ApiKey fake_api_key",
        endpoint="https://localhost/public/v1",
    )


@pytest.fixture
def logger(mocker):
    return mocker.MagicMock()


@pytest.fixture(scope="session", autouse=True)
def mock_settings_env_vars():
    with mock.patch.dict(
        os.environ,
        {
            "API_KEY": "ApiKey fake",
            "SERVER_ADDRESS": "api.test.wow",
            "ENVIRONMENT_ID": "ENV-123",
            "DATABASE_URL": "sqlite:///:memory:",
        },
        clear=True,
    ):
        yield


register(MyModelFactory)
register(RelatedModelFactory)
register(TransactionalModelFactory)
