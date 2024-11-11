# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""

from symposium.connectors.gemini_google import gemini_get_client, gemini_complete, gemini_get_chat_session, gemini_message
from grammateus.entities import Grammateus
from yaml import safe_load as yl


grammateus = Grammateus(origin='gemini', location='convers.log')

system_instruction = 'Your are a language model.'


client_kwargs =f""" # this is a yaml text
    model:          gemini-1.5-flash-latest  # name of the model
    tools:          ~  # comma separated list of tools or ~ or null
    tool_config:    ~
    system:         {system_instruction}  # https://ai.google.dev/gemini-api/docs/system-instructions?hl=en
"""

client = gemini_get_client(**yl(client_kwargs))

generation_configuration = {
    'n':                1,
    'stop_sequences':   ['stop'],
    'max_tokens':       5000,
    'temperature':      0.5,
    'top_p':            0.5,
    'top_k':            1,
    'mime_type':        "text/plain",
    'schema':           None
}

completion_kwargs = {
    'prompt': 'Can human nature be changed?',
    'generation_config': generation_configuration,
    "stream": False,
}

# resp = gemini_complete(client=client,
#                        recorder=grammateus,
#                        **completion_kwargs)
#
# print('ok')

messages = {
    "role":"user",
    "parts":[
        {"text":"can human nature be changed?"},
        {"text":"Tell me in one sentence."}
    ]
}

chat = gemini_get_chat_session(client=client)

message_kwargs = {
    'messages': messages,
    'generation_config': generation_configuration,
    'stream': False,
    'tools': None,
    'tool_config': None
}

message = gemini_message(chat_session=chat,
                         recorder=grammateus,
                         **message_kwargs)
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