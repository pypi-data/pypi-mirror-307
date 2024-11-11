# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import dotenv
dotenv.load_dotenv()
import symposium.connectors.openai_native as openai
import pytest


@pytest.fixture
def openai_client():
    return openai.get_openai_client()


def test_get_openai_client():
    client = openai.get_openai_client()
    assert client is not None
