# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""

from typing import List, Dict
from os import environ
import requests
from ..adapters.tog_lma import prepared_together_messages, formatted_together_output, formatted_together_completion, prepared_together_prompt


api_key             = environ.get("TOGETHER_API_KEY",)
api_base            = environ.get("TOGETHER_BASE_URL", "https://api.together.xyz/v1")
default_model       = environ.get("TOGETHER_DEFAULT_MODEL", "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo")
completion_model    = environ.get("TOGETHER_COMPLETION_MODEL","meta-llama/Meta-Llama-3-70B")

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + api_key
}


def get_together_client(**kwargs):
    client = None
    client_kwargs = {
        "timeout":      kwargs.get("timeout", 100.0),
        "max_retries":  kwargs.get("max_retries", 3),
    }
    try:
        import together
        client = together.Together(**client_kwargs)
    except ImportError:
        print("groq package is not installed")
    return client

def together_complete(client, messages, recorder=None, **kwargs):
    """ All parameters should be in kwargs, but they are optional
    """
    record, formatted_prompt = prepared_together_prompt(
        kwargs.get("messages", messages)
    )
    kwa = {
        "model":                kwargs.get("model", completion_model),
        "max_tokens_to_sample": kwargs.get("max_tokens", 1),
        "prompt":               formatted_prompt,
        "stop_sequences":       kwargs.get("stop_sequences", ["stop"]),
        "temperature":          kwargs.get("temperature", 0.5),
        "top_k":                kwargs.get("top_k", 250),
        "top_p":                kwargs.get("top_p", 0.5),
        "metadata":             kwargs.get("metadata", None)
    }
    try:
        completion = client.completions.create(**kwa)
        completion_dump = completion.model_dump()
        if recorder:
            log_message = {"query": kwa, "response": {"message": completion_dump}}
            recorder.log_event(log_message)
    except Exception as e:
        print(e)
        return None
    formatted = formatted_together_completion(completion_dump)
    if recorder:
        rec = {"messages": record, "response": formatted}
        recorder.record(rec)
    return formatted


def together_message(client, messages, recorder=None, json=True, **kwargs):
    """ All parameters should be in kwargs, but they are optional
    """
    record, formatted_messages = prepared_together_messages(
        kwargs.get("messages", messages)
    )
    chat_kwargs = {
        "model":            kwargs.get("model", default_model),
        "messages":         formatted_messages,
        "max_tokens":       kwargs.get("max_tokens", 5),
        "n":                kwargs.get("n", 1),
        "stop":             kwargs.get("stop_sequences", ["stop"]),
        "response_format":  kwargs.get("response_format", None),
        # "tools":            kwargs.get("tools", None),
        # "tool_choice":      kwargs.get("tool_choice", "auto"),
        # "seed":             kwargs.get("seed", None),
        "frequency_penalty": kwargs.get("frequency_penalty", None),
        "presence_penalty": kwargs.get("presence_penalty", None),
        "logit_bias":       kwargs.get("logit_bias", None),
        "logprobs":         kwargs.get("logprobs", None),
        # "top_logprobs":     kwargs.get("top_logprobs", None),
        "temperature":      kwargs.get("temperature", 0.5),
        "top_p":            kwargs.get("top_p", 0.5),
        # "user":             kwargs.get("user", None)
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
