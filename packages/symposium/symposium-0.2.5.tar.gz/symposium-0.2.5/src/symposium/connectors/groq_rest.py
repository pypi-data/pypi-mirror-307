# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from typing import List, Dict
from os import environ
import requests
from ..adapters.grq_rest import prepared_grq_messages, format_grq_output


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


def grq_message(messages,
                recorder,
                **kwargs):

    """A simple requests call to ChatGPT chat completions endpoint.
        kwargs:
            temperature     = 0 to 1.0
            top_p           = 0.0 to 1.0
            n               = 1 to ...
            frequency_penalty = -2.0 to 2.0
            presence_penalty = -2.0 to 2.0
            max_tokens      = number of tokens
    """
    record, formatted_messages = prepared_grq_messages(
        kwargs.get("messages", messages)
    )
    json_data = {
        "model":            kwargs.get("model", default_model),
        "messages":         formatted_messages,
        "max_tokens":       kwargs.get("max_tokens", 5),
        "n":                kwargs.get("n", 1),
        "stop":             kwargs.get("stop_sequences", ["stop"]),
        "response_format":  kwargs.get("response_format", None),
        "tools":            kwargs.get("tools", None),
        "tool_choice":      kwargs.get("tool_choice", "auto"),
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
        response = requests.post(
            f"{api_base}/chat/completions",
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
        formatted, other = format_grq_output(msg_dump)
        if other:
            formatted["other"] = other
        if recorder:
            rec = {"messages": record, "response": formatted}
            recorder.record(rec)
        return formatted

    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return None


def grq_models() -> List:
    """Returns a list of available models."""
    models_list = []
    try:
        response = requests.get(f"{api_base}/models",
                                headers=headers)
        if response.status_code == requests.codes.ok:
            for model in response.json()['data']:
                models_list.append(model['id'])
            return models_list
        else:
            print(f"Request status code: {response.status_code}")
            return []
    except Exception as e:
        print("Unable to generate Models response")
        print(f"Exception: {e}")
        return models_list


if __name__ == '__main__':
    print('You launched main.')