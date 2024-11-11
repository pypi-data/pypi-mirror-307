# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from symposium.connectors.anthropic_rest import claud_complete, claud_message
from grammateus.entities import Grammateus
from yaml import safe_load as yl

messages = f"""     # this is a string in YAML format, f is used for parameters
    - role:  human  # not the idiotic 'user', God forbid.
      name:  Alex 
      content: Can we change human nature?
"""
messages_dict = yl(messages)

grammateus = Grammateus(origin='anthropic', location='convers.log')

kwargs = f"""       # this is a string in YAML format, f is used for parameters
    model:          claude-3-sonnet-20240229
    system:         Always answer concisely
    messages:       {messages}
    max_tokens:     10
    stop_sequences:
      - stop
      - "\n\n\nHuman:"
    stream:         False
    temperature:    0.5
    top_k:          10
    top_p:          0.5
"""
kwargs_dict = yl(kwargs)

message = claud_message(
    # messages=yl(messages),
    recorder=grammateus,
    **yl(kwargs)
)

if message is not None:
    response=message['content']

kwargs_dict['model'] = 'claude-instant-1.2'

message = claud_complete(
    # messages=yl(messages),
    recorder=grammateus,
    **kwargs_dict
)
if message is not None:
    response = message['content']


if __name__ == '__main__':
    print('ok')