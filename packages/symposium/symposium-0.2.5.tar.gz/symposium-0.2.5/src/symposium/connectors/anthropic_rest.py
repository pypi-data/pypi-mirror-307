# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from os import environ
import requests
from ..adapters.anth import (prepared_ant_messages,
                             formatted_ant_output,
                             prepared_ant_prompt,
                             formatted_ant_completion)

api_key             = environ.get("ANTHROPIC_API_KEY")
organization        = environ.get("ANTHROPIC_ORGANIZATION", "")
api_base            = environ.get("ANTHROPIC_API_BASE", "https://api.anthropic.com/v1")
api_type            = environ.get("ANTHROPIC_VERSION", "2023-06-01")
default_model       = environ.get("ANTHROPIC_DEFAULT_MODEL", "claude-instant-1.2")
completion_model    = environ.get("ANTHROPIC_COMPLETION_MODEL",'claude-instant-1.2')
message_model       = environ.get("ANTHROPIC_MESSAGE_MODEL",'claude-3-sonnet-20240229')
# claude-3-opus-20240229, claude-3-sonnet-20240229

headers = {
    "x-api-key": api_key,
    "anthropic-version": "2023-06-01",
    "content-type": "application/json"
}

HUMAN_PREFIX        = "\n\nHuman:"
MACHINE_PREFIX      = "\n\nAssistant:"


def claud_complete(messages=None, recorder=None, **kwargs):
    """ All parameters should be in kwargs, but they are optional
    """
    record, formatted_prompt = prepared_ant_prompt(
        kwargs.get("messages", messages)
    )
    json_data = {
        "model":                kwargs.get("model", completion_model),
        "max_tokens_to_sample": kwargs.get("max_tokens", 1),
        "prompt":               formatted_prompt,
        "stop_sequences":       kwargs.get("stop_sequences",[HUMAN_PREFIX]),
        "temperature":          kwargs.get("temperature", 0.5),
        "top_k":                kwargs.get("top_k", 250),
        "top_p":                kwargs.get("top_p", 0.5),
        "metadata":             kwargs.get("metadata", None)
    }
    try:
        response = requests.post(
            f"{api_base}/complete",
            headers=headers,
            json=json_data,
        )
        if response.status_code == requests.codes.ok:
            completion_dump = response.json()
            if recorder:
                log_message = {"query": json_data, "response": {"message": completion_dump}}
                recorder.log_event(log_message)
        else:
            print(f"Request status code: {response.status_code}")
            completion_dump = None
        formatted = formatted_ant_completion(completion_dump)
        if recorder:
            rec = {"messages": record, "response": formatted}
            recorder.record(rec)
        return formatted
    except Exception as e:
        print("Unable to generate Completions response")
        print(f"Exception: {e}")
        return None


def claud_message(messages=None, recorder=None, **kwargs):
    """ All parameters should be in kwargs, but they are optional
    """
    record, formatted_messages = prepared_ant_messages(
        kwargs.get("messages", messages)
    )
    json_data = {
        "model":                kwargs.get("model", message_model),
        "system":               kwargs.get("system", "answer concisely"),
        "messages":             formatted_messages,
        "max_tokens":           kwargs.get("max_tokens", 1),
        "stop_sequences":       kwargs.get("stop_sequences",['stop', HUMAN_PREFIX]),
        "stream":               kwargs.get("stream", False),
        "temperature":          kwargs.get("temperature", 0.5),
        "top_k":                kwargs.get("top_k", 250),
        "top_p":                kwargs.get("top_p", 0.5),
        "metadata":             kwargs.get("metadata", None)
    }
    try:
        response = requests.post(
            f"{api_base}/messages",
            headers=headers,
            json=json_data,
        )
        if response.status_code == requests.codes.ok:
            msg_dump = response.json()
            if recorder:
                log_message = {"query": json_data, "response": {"message": msg_dump}}
                recorder.log_event(log_message)
        else:
            print(f"Request status code: {response.status_code}")
            return None
        formatted = formatted_ant_output(msg_dump)
        if recorder:
            rec = {"messages": record, "response": formatted}
            recorder.record(rec)
        return formatted

    except Exception as e:
        print("Unable to generate Message response")
        print(f"Exception: {e}")
        return None


if __name__ == "__main__":
    print("you launched main.")
