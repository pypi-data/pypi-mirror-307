# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from symposium.connectors.gemini_rest import gemini_message
from grammateus.entities import Grammateus


grammateus = Grammateus(origin='gemini', location='convers.log')

messages = [
        {"role":"human", "name":"alex", "content":"Put your name between the <name></name> tags."},
]
kwargs = {
    "model": "gemini-1.5-flash-latest",
    "max_tokens": 256
}

message = gemini_message(
    messages=messages,
    recorder=grammateus,
    **kwargs
)
response=message
print('ok')

"""
contents = [
        {
            "parts": [
                {"text": "Create a most concise text possible, preferrably just one sentence, answering the question: Can human nature be changed?"}
            ]
        }
    ]
contents = [
    {
        "role": "user",
        "parts": [
            {"text": "Human nature can not be changed, because..."},
            {"text": "...and that is why human nature can not be changed."}
        ]
    },{
        "role": "model",
        "parts": [
            {"text": "Should I synthesize a text that will be placed between these two statements and follow the previous instruction while doing that?"}
        ]
    },{
        "role": "user",
        "parts": [
            {"text": "Yes, please do."},
            {"text": "Create a most concise text possible, preferably just one sentence}"}
        ]
    }
]
    kwa = {
        "model": "gemini-1.5-pro",
        "temperature": 1.0,
        "max_tokens": 1000,
        "n": 1,
        "top_p": 0.9,
        "top_k": 50
    }

    a = gemini_message(messages=contents, **kwa)
    # contents = [
    #     {
    #         "role": "user",
    #         "parts": [
    #             {"text": "Can human nature be changed?"},
    #         ]
    #     }
    # ]
    # kwa = {
    #     "temperature": 1.0
    # }
    # a = gemini_answer(contents=contents, **kwa)

"""