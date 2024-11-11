# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import dotenv
dotenv.load_dotenv()
from symposium.connectors import anthropic_rest as ant


def test_claud_message():
    messages = [
        {"role": "user", "content": "Can we change human nature, yes or no?"}
    ]
    kwargs = {
        "model": "claude-3-sonnet-20240229",
        "system": "answer concisely",
        # "messages":             [],
        "max_tokens": 3,
        "stop_sequences": ["stop", ant.HUMAN_PREFIX],
        "stream": False,
        "temperature": 0.5,
        "top_k": 250,
        "top_p": 0.5
    }
    response = ant.claud_message(messages, **kwargs)
    assert True


def test_claud_message_kwargs():
    kwargs = {
        "model": "claude-3-sonnet-20240229",
        "system": "answer concisely",
        "messages":[
            {"role": "user", "content": "Can we change human nature, yes or no?"}],
        "max_tokens": 3,
        "stop_sequences": ["stop", ant.HUMAN_PREFIX],
        "stream": False,
        "temperature": 0.5,
        "top_k": 250,
        "top_p": 0.5
    }
    response = ant.claud_message(**kwargs)
    assert True
