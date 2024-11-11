# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from typing import List, Dict
from os import environ
import requests
from ..adapters.grq_native import prepared_grq_messages, format_grq_output


api_key             = environ.get("GROQ_API_KEY")
api_key_path        = environ.get("GROQ_API_KEY_PATH")

organization        = environ.get("GROQ_ORGANIZATION")
organization_id     = environ.get("GROQ_ORGANIZATION_ID")
api_base            = environ.get("GROQ_API_BASE", "https://api.groq.com/openai/v1")
api_type            = environ.get("GROQ_API_TYPE", "open_ai")
default_model       = environ.get("GROQ_DEFAULT_MODEL", "mixtral-8x7b-32768")
completion_model    = environ.get("GROQ_COMPLETION_MODEL",'mixtral-8x7b-32768')

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + api_key,
    "Organization": organization
}


def get_groq_client(**kwargs):
    client = None
    client_kwargs = {
        "timeout":      kwargs.get("timeout", 100.0),
        "max_retries":  kwargs.get("max_retries", 3),
    }
    try:
        import groq
        client = groq.Groq(**client_kwargs)
    except ImportError:
        print("groq package is not installed")
    return client


def grq_message(client, messages, recorder=None, json=True, **kwargs):
    """ All parameters should be in kwargs, but they are optional
    """
    record, formatted_messages = prepared_grq_messages(
        kwargs.get("messages", messages)
    )
    chat_kwargs = {
        "model":            kwargs.get("model", default_model),
        "messages":         formatted_messages,
        "max_tokens":       kwargs.get("max_tokens", 5),
        "n":                kwargs.get("n", 1),
        "stop":             kwargs.get("stop_sequences", ["stop"]),
        "response_format":  kwargs.get("response_format", None),
        "tools":            kwargs.get("tools", None),
        "tool_choice":      kwargs.get("tool_choice", "auto"),
        "seed":             kwargs.get("seed", None),
        "frequency_penalty": kwargs.get("frequency_penalty", None),
        "presence_penalty": kwargs.get("presence_penalty", None),
        "logit_bias":       kwargs.get("logit_bias", None),
        "logprobs":         kwargs.get("logprobs", None),
        "top_logprobs":     kwargs.get("top_logprobs", None),
        "temperature":      kwargs.get("temperature", 0.5),
        "top_p":            kwargs.get("top_p", 0.5),
        "user":             kwargs.get("user", None)
        }
    try:
        msg = client.chat.completions.create(**chat_kwargs)
        msg_dump = msg.model_dump()
        if recorder:
            log_message = {"query": chat_kwargs, "response": {"message": msg_dump}}
            recorder.log_event(log_message)
    except Exception as e:
        print(e)
        return None
    if recorder:
        rec = {'messages': chat_kwargs['messages'], 'response': msg_dump['choices']}
        recorder.record(rec)
    if json:
        return msg_dump
    else:
        return msg


if __name__ == '__main__':
    print('You launched main.')