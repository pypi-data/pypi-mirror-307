# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from symposium.connectors.groq_native import grq_message, get_groq_client
from grammateus.entities import Grammateus
from yaml import safe_load as yl


# mod = grq_models()
grammateus = Grammateus(origin='groq', location='conversation_test.log')

client_kwargs = f"""    # this is a yaml text
    timeout:      120.0
    max_retries:  4  # default is 3
"""

client = get_groq_client(**yl(client_kwargs))

messages = """
    - role: human
      name: alex
      content: Tell me who was Gerhard Gentzen and how he died.
"""
kwargs = """
    model: llama-3.1-70b-versatile
    max_tokens: 8000
    n: 1
    stop_sequences: [stop, <|eot_id|>]
"""

kwa = yl(kwargs)

message = grq_message(
    client=client,
    messages=yl(messages),
    recorder=grammateus,
    **yl(kwargs)
)
response=message


if __name__ == "__main__":
    print("You launched main.")


