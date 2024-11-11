# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import os
from symposium.connectors.cohere_native import get_cohere_client, cohere_complete, cohere_message
from grammateus.entities import Grammateus


grammateus = Grammateus(origin='cohere', location='convers.log')
kwa = {
    "timeout": 320.0,
}
coh = get_cohere_client(**kwa)
messages = [
    {'role': 'user', 'content': 'Hello'},
    {'role': 'machine', 'content': 'Hi, How are you?'},
    {'role': 'user', 'content': 'I am fine. Tell me your name.'}
]
message = cohere_message(
    client=coh,
    messages=messages,
    recorder=grammateus
)
response=message

prompt = 'Hello'
completion = cohere_complete(
    coh,
    prompt,
    recorder=grammateus
)
response = completion['choices']


if __name__ == "__main__":
    print("ok")

