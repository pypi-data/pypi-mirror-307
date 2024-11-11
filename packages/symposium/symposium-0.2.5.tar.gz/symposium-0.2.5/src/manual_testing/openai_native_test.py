# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import os
from symposium.connectors.openai_native import get_openai_client, openai_complete, openai_message
from grammateus.entities import Grammateus


grammateus = Grammateus(origin='openai', location='convers.log')
oai = get_openai_client()
messages = [
    {'role': 'user','content': 'Hello'}
]
message = openai_message(
    client=oai,
    messages=messages,
    recorder=grammateus
)
response=message

prompt = 'Hello'
completion = openai_complete(
    oai,
    prompt,
    recorder=grammateus
)
response = completion['choices']


if __name__ == "__main__":
    print("ok")

