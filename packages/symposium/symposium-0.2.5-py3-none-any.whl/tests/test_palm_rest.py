# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import dotenv
dotenv.load_dotenv()
from symposium.connectors import palm_rest as palm
import pytest


def test_palm_message(self):
    context = "This conversation will be happening between Albert and Niels"
    examples = [
        {
            "input": {"author": "Albert", "content": "We didn't talk about the quantum mechanics lately..."},
            "output": {"author": "Niels", "content": "Yes indeed."}
        }
    ]
    messages = [
        {
            "author": "Albert",
            "content": "Can we change human nature?"
        }, {
            "author": "Niels",
            "content": "Not clear..."
        }, {
            "author": "Albert",
            "content": "Seriously, can we?"
        }
    ]
    kwargs = {
        "n": 1,
        "top_k": 100
    }
    a = palm.palm_message(context, examples, messages, **kwargs)
    assert True


def test_palm_message_kwargs(self):
    kwargs = {
        "context": "This conversation will be happening between Albert and Niels",
        "examples": [
            {
                "input": {"author": "Albert", "content": "We didn't talk about the quantum mechanics lately..."},
                "output": {"author": "Niels", "content": "Yes indeed."}
            }
        ],
        "messages": [
            {
                "author": "Albert",
                "content": "Can we change human nature?"
            }, {
                "author": "Niels",
                "content": "Not clear..."
            }, {
                "author": "Albert",
                "content": "Seriously, can we?"
            }
        ],
        "n": 1,
        "top_k": 100
    }
    a = palm.palm_message(**kwargs)
    assert True
