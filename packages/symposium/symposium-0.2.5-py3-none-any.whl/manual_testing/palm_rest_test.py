# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from symposium.connectors.palm_rest import palm_complete, palm_message
from grammateus.entities import Grammateus


grammateus = Grammateus(origin='palm', location='test_conversations.log')

# messages = [
#         {"role":"human", "name":"alex", "content":"Put your name between the <name></name> tags."},
# ]
# kwargs = {
#     "max_tokens": 256,
#     "n": 1
# }
# message = palm_complete(
#     messages=messages,
#     recorder=grammateus,
#     **kwargs
# )
# response=message

context = "This conversation will be happening between Albert and Niels"
examples = [
        {
            "input": {"author": "Albert", "content": "We didn't talk about quantum mechanics lately..."},
            "output": {"author": "Niels", "content": "Yes, indeed."}
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
    "model": "chat-bison-001",
    # "context": str,
    # "examples": [],
    # "messages": [],
    "temperature": 0.5,
    # no 'max_tokens', beware the effects of that!
    "n": 1,
    "top_p": 0.5,
    "top_k": None
}
responses = palm_message(messages=messages, context=context, examples=examples, **kwargs)

print('ok')

"""
context = "This conversation will be happening between Albert and Niels"
examples = [
        {
            "input": {"author": "Albert", "content": "We didn't talk about quantum mechanics lately..."},
            "output": {"author": "Niels", "content": "Yes, indeed."}
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
    "model": "chat-bison-001",
    # "context": str,
    # "examples": [],
    # "messages": [],
    "temperature": 0.5,
    # no 'max_tokens', beware the effects of that!
    "n": 1,
    "top_p": 0.5,
    "top_k": None
}
"""