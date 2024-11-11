# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from os import environ


api_key             = environ.get("XAI_API_KEY")
api_key_path        = environ.get("XAI_API_KEY_PATH")

organization        = environ.get("XAI_ORGANIZATION")
organization_id     = environ.get("XAI_ORGANIZATION_ID")
api_base            = environ.get("XAI_API_BASE", "https://api.x.ai/v1")
api_type            = environ.get("XAI_API_TYPE", "open_ai")
default_model       = environ.get("XAI_DEFAULT_MODEL", "grok-beta")
completion_model    = environ.get("XAI_COMPLETION_MODEL",'grok-beta')
embedding_model     = environ.get("XAI_EMBEDDING_MODEL",'')  # text-similarity-davinci-001


def get_xai_openai_client(**kwargs):
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key, base_url=api_base)
    except ImportError:
        print("openai package is not installed       ```pip install symposium[openai]")
        return None
    return client


def xai_openai_complete(client, prompt, recorder=None, json=False, **kwargs):
    """ All parameters should be in kwargs, but they are optional
    """
    kwa = {
        "model":            kwargs.get("model", completion_model),
        "max_tokens":       kwargs.get("max_tokens_to_sample", 5),
        "prompt":           kwargs.get("prompt", prompt),
        "suffix":           kwargs.get("suffix", None),
        "stop":             kwargs.get("stop_sequences", ["stop"]),
        "n":                kwargs.get("n", 1),
        "best_of":          kwargs.get("best_of", 1),
        "seed":             kwargs.get("seed", None),
        "frequency_penalty":kwargs.get("frequency_penalty", None),
        "presence_penalty": kwargs.get("presence_penalty", None),
        "logit_bias":       kwargs.get("logit_bias", {}),
        "logprobs":         kwargs.get("logprobs", None),
        "temperature":      kwargs.get("temperature", 0.5),
        "top_p":            kwargs.get("top_p", 0.5),
        # "user":             kwargs.get("user", None)
    }
    try:
        completion = client.completions.create(**kwa)
        completion_dump = completion.model_dump()
        if recorder:
            log_message = {"query": kwa, "response": {"completion": completion_dump}}
            recorder.log_event(log_message)
    except Exception as e:
        print(e)
        return None
    if recorder:
        rec = {"prompt": kwa["prompt"], "completion": completion_dump['choices']}
        recorder.record(rec)
    if json:
        return completion_dump
    else:
        return completion


def xai_openai_message(client, messages, recorder=None, json=False, **kwargs):
    """ All parameters should be in kwargs, but they are optional
    """
    kwa = {
        "model":            kwargs.get("model", default_model),
        "messages":         kwargs.get("messages", messages),
        "max_tokens":       kwargs.get("max_tokens_to_sample", 1),
        "stop":             kwargs.get("stop_sequences", ["stop"]),
        "response_format":  kwargs.get("response_format", None),
        "tools":            kwargs.get("tools", None),
        "tool_choice":      kwargs.get("tool_choice", None),
        "seed":             kwargs.get("seed", None),
        "frequency_penalty":kwargs.get("frequency_penalty", None),
        "presence_penalty": kwargs.get("presence_penalty", None),
        "logit_bias":       kwargs.get("logit_bias", None),
        "logprobs":         kwargs.get("logprobs", None),
        "top_logprobs":     kwargs.get("top_logprobs", None),
        "temperature":      kwargs.get("temperature", 0.5),
        "top_p":            kwargs.get("top_p", 0.5),
        "user":             kwargs.get("user", None)
    }
    try:
        msg = client.chat.completions.create(**kwa)
        msg_dump = msg.model_dump()
        if recorder:
            log_message = {"query": kwa, "response": {"message": msg_dump}}
            recorder.log_event(log_message)
    except Exception as e:
        print(e)
        return None
    if recorder:
        rec = {'messages': kwa['messages'], 'response': msg_dump['choices']}
        recorder.record(rec)
    if json:
        return msg_dump
    else:
        return msg


if __name__ == "__main__":
    from grammateus.entities import Grammateus
    recorder = Grammateus(origin='openai', location='convers.log')
    client = get_xai_openai_client()
    completion = xai_openai_message(client, messages=[{"role": "user", "content": "Hello"}], recorder=recorder)
    print("ok")

'''
            model           =kwargs.get("model", completion_model),
            max_tokens      =kwargs.get("max_tokens_to_sample", 5),
            prompt          =kwargs.get("prompt", prompt),
            suffix          =kwargs.get("suffix", None),
            stop            =kwargs.get("stop_sequences",["stop"]),
            n               =kwargs.get("n", 1),
            best_of         =kwargs.get("best_of", 1),
            seed            =kwargs.get("seed", None),
            frequency_penalty=kwargs.get("frequency_penalty", None),
            presence_penalty=kwargs.get("presence_penalty", None),
            logit_bias      =kwargs.get("logit_bias", None),
            logprobs        =kwargs.get("logprobs", None),
            temperature     =kwargs.get("temperature", 0.5),
            top_p           =kwargs.get("top_p", 0.5),
            user            =kwargs.get("user", None)
'''
'''
            model           =kwargs.get("model", default_model),
            messages        =messages,
            max_tokens      =kwargs.get("max_tokens_to_sample", 5),
            stop            =kwargs.get("stop_sequences", ["stop"]),
            response_format =kwargs.get("response_format", None),
            tools           =kwargs.get("tools", None),
            tool_choice     =kwargs.get("tool_choice", None),
            seed            =kwargs.get("seed", None),
            frequency_penalty=kwargs.get("frequency_penalty", None),
            presence_penalty=kwargs.get("presence_penalty", None),
            logit_bias      =kwargs.get("logit_bias", None),
            logprobs        =kwargs.get("logprobs", None),
            top_logprobs    =kwargs.get("top_logprobs", None),
            temperature     =kwargs.get("temperature", 0.5),
            top_p           =kwargs.get("top_p", 0.5),
            user            =kwargs.get("user", None)
'''