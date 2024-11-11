# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import os
from symposium.connectors.anthropic_native import get_claud_client, claud_complete, claud_message
from grammateus.entities import Grammateus

grammateus = Grammateus(origin='anthropic', location='convers.log')

client_kwargs = {
    "api_key": None,
    "auth_token": None,
    "base_url": None,
    "timeout": 100.0,
    "max_retries": 3,
    "default_query": None,
    "http_client": None,
    "transport": None,
    "connection_pool_limits": None,
    "_strict_response_validation": False
}
ant = get_claud_client(**client_kwargs)

messages = [
    {'role': 'human', 'name': 'alex', 'content': 'Put your name between the <name></name> tags.'},
]
# kwargs = {
#     "system": "be an Abstract Intellect.",
#     "max_tokens": 256
# }
# anthropic_message = claud_message(
#     client=ant,
#     messages=messages,
#     recorder=grammateus,
#     **kwargs
# )
# if anthropic_message is not None:
#     response=anthropic_message['content']

kwargs = {
    "max_tokens": 256
}
anthropic_complete = claud_complete(
    client=ant,
    messages=messages,
    recorder=grammateus,
    **kwargs
)
if anthropic_complete is not None:
    completion = anthropic_complete['content']

if __name__ == '__main__':
    print('ok')