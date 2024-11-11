# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from os import environ
from ..adapters.anth import (prepared_ant_messages,
                             formatted_ant_output,
                             prepared_ant_prompt,
                             formatted_ant_completion)


default_model       = environ.get("ANTHROPIC_DEFAULT_MODEL", "claude-instant-1.2")
completion_model    = environ.get("ANTHROPIC_COMPLETION_MODEL",'claude-instant-1.2')
message_model       = environ.get("ANTHROPIC_MESSAGE_MODEL",'claude-3-sonnet-20240229')
# claude-3-opus-20240229, claude-3-sonnet-20240229

HUMAN_PREFIX = "\n\nHuman:"
MACHINE_PREFIX = "\n\nAssistant:"


def get_claud_client(**kwargs):
    client = None
    client_kwargs = {
        "timeout":      kwargs.get("timeout", 100.0),
        "max_retries":  kwargs.get("max_retries", 3),
    }
    try:
        import anthropic
        client = anthropic.Anthropic(**client_kwargs)
    except ImportError:
        print("anthropic package is not installed")
    return client


def claud_complete(client, messages, recorder=None, **kwargs):
    """ All parameters should be in kwargs, but they are optional
    """
    record, formatted_prompt = prepared_ant_prompt(
        kwargs.get("messages", messages)
    )
    kwa = {
        "model":                kwargs.get("model", completion_model),
        "max_tokens_to_sample": kwargs.get("max_tokens", 1),
        "prompt":               formatted_prompt,
        "stop_sequences":       kwargs.get("stop_sequences", [HUMAN_PREFIX]),
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
    formatted = formatted_ant_completion(completion_dump)
    if recorder:
        rec = {"messages": record, "response": formatted}
        recorder.record(rec)
    return formatted


def claud_message(client, messages, recorder=None, **kwargs):
    """ All parameters should be in kwargs, but they are optional
    """
    record, formatted_messages = prepared_ant_messages(
        kwargs.get("messages", messages)
    )
    kwa = {
        "model":                kwargs.get("model", message_model),
        "system":               kwargs.get("system", "answer concisely"),
        "messages":             formatted_messages,
        "max_tokens":           kwargs.get("max_tokens", 1),
        "stop_sequences":       kwargs.get("stop_sequences", ['stop', HUMAN_PREFIX]),
        "stream":               kwargs.get("stream", False),
        "temperature":          kwargs.get("temperature", 0.5),
        "top_k":                kwargs.get("top_k", 250),
        "top_p":                kwargs.get("top_p", 0.5),
        "metadata":             kwargs.get("metadata", None)
    }
    try:
        msg = client.messages.create(**kwa)
        msg_dump = msg.model_dump()
        if recorder:
            log_message = {"query": kwa, "response": {"message": msg_dump}}
            recorder.log_event(log_message)
    except Exception as e:
        print(e)
        return None
    formatted = formatted_ant_output(msg_dump)
    if recorder:
        rec = {"messages": record, "response": formatted}
        recorder.record(rec)
    return formatted


if __name__ == "__main__":
    print("you launched main.")

'''
            model=kwargs.get("model", "claude-instant-1.2"),
            max_tokens_to_sample=kwargs.get("max_tokens_to_sample", 5),
            prompt=f"{HUMAN_PREFIX}{prompt}{MACHINE_PREFIX}",
            stop_sequences=kwargs.get(
                "stop_sequences",
                [HUMAN_PREFIX]),
            temperature=kwargs.get("temperature", 0.5),
            top_k=kwargs.get("top_k", 250),
            top_p=kwargs.get("top_p", 0.5),
            stream=kwargs.get("stream", False),
            metadata=kwargs.get("metadata", None)
'''
'''
            model=kwargs.get("model", "claude-3-sonnet-20240229"),
            system=kwargs.get("system", "answer concisely"),
            messages=messages,
            max_tokens=kwargs.get("max_tokens", 1),
            stop_sequences=kwargs.get(
                "stop_sequences",
                [HUMAN_PREFIX]),
            stream=kwargs.get("stream", False),
            temperature=kwargs.get("temperature", 0.5),
            top_k=kwargs.get("top_k", 250),
            top_p=kwargs.get("top_p", 0.5),
            metadata=kwargs.get("metadata", None)
        
'''