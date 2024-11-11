# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import os
from symposium.connectors.xai_openai_native import get_xai_openai_client, xai_openai_complete, xai_openai_message
from grammateus.entities import Grammateus


grammateus = Grammateus(origin='xai', location='convers.log')
xai_openai = get_xai_openai_client()
messages = [
    {'role': 'user','content': 'Hello'}
]
kwargs = {
    "max_tokens_to_sample": 100
}
message = xai_openai_message(
    client=xai_openai,
    messages=messages,
    recorder=grammateus,
    **kwargs
)
response=message

prompt = 'Hello'
completion = xai_openai_complete(
    xai_openai,
    prompt,
    recorder=grammateus,
    **kwargs
)
other_response = completion['choices']


if __name__ == "__main__":
    print("ok")

