# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from typing import List, Dict
from os import environ
import requests
from ..adapters.oai_rest import prepared_oai_messages, format_oai_output


api_key             = environ.get("OPENAI_API_KEY")
api_key_path        = environ.get("OPENAI_API_KEY_PATH")

organization        = environ.get("OPENAI_ORGANIZATION")
organization_id     = environ.get("OPENAI_ORGANIZATION_ID")
api_base            = environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")
api_type            = environ.get("OPENAI_API_TYPE", "open_ai")
default_model       = environ.get("OPENAI_DEFAULT_MODEL", "gpt-3.5-turbo")
completion_model    = environ.get("OPENAI_COMPLETION_MODEL",'gpt-3.5-turbo-instruct')
embedding_model     = environ.get("OPENAI_EMBEDDING_MODEL",'text-embedding-3-small')  # text-similarity-davinci-001

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + api_key,
    "Organization": organization
}


def gpt_message(messages,
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
    record, formatted_messages = prepared_oai_messages(
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
        formatted, other = format_oai_output(msg_dump)
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


def gpt_fill_in(text_before, text_after, **kwargs):
    """A specialized completions request.
        kwargs:
            temperature     = 0 to 1.0
            top_p           = 0.0 to 1.0
            n               = 1 to ...
            best_of         = 4
            frequency_penalty = -2.0 to 2.0
            presence_penalty = -2.0 to 2.0
            max_tokens      = number of tokens
            stop = ["stop"]  # array of up to 4 sequences
    """
    responses = []
    json_data = {
        "model":            kwargs.get("model", completion_model),
        "prompt":           text_before,
        "suffix":           text_after,
        "max_tokens":       kwargs.get("max_tokens", 5),
        "n":                kwargs.get("n", 1),
        "best_of":          kwargs.get("best_of", 1),
        "stop":             kwargs.get("stop_sequences", ["stop"]),
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
            f"{api_base}/completions",
            headers=headers,
            json=json_data,
        )
        if response.status_code == requests.codes.ok:
            for choice in response.json()['choices']:
                responses.append(choice)
        else:
            print(f"Request status code: {response.status_code}")
        return responses
    except Exception as e:
        print("Unable to generate Insertion response")
        print(f"Exception: {e}")
        return responses


def gpt_complete(prompt, **kwargs) -> List:
    """A completions endpoint call through requests.
        kwargs:
            temperature     = 0 to 1.0
            top_p           = 0.0 to 1.0
            n               = 1 to ...
            best_of         = 4
            frequency_penalty = -2.0 to 2.0
            presence_penalty = -2.0 to 2.0
            max_tokens      = number of tokens
            logprobs        = number up to 5
            stop            = ["stop"]  array of up to 4 sequences
            logit_bias      = map token: bias -1.0 to 1.0 (restrictive -100 to 100)
    """
    responses = []
    json_data = {
        "model":            kwargs.get("model", completion_model),
        "prompt":           kwargs.get("prompt", prompt),
        "suffix":           kwargs.get("suffix", None),
        "max_tokens":       kwargs.get("max_tokens", 5),
        "n":                kwargs.get("n", 1),
        "best_of":          kwargs.get("best_of", 1),
        "stop":             kwargs.get("stop_sequences", ["stop"]),
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
            f"{api_base}/completions",
            headers=headers,
            json=json_data,
        )
        if response.status_code == requests.codes.ok:
            for choice in response.json()['choices']:
                responses.append(choice)
        else:
            print(f"Request status code: {response.status_code}")
        return responses
    except Exception as e:
        print("Unable to generate Completions response")
        print(f"Exception: {e}")
        return responses


def gpt_embeddings(input_list: List[str], model=embedding_model, **kwargs) -> List[Dict]:
    """Returns the embedding of a text string.
        kwargs:
        user = string
    """
    embeddings_list = []
    json_data = {"model": model, "input": input_list} | kwargs
    try:
        response = requests.post(
            f"{api_base}/embeddings",
            headers=headers,
            json=json_data,
        )
        if response.status_code == requests.codes.ok:
            embeddings_list = response.json()['data']
        else:
            print(f"Request status code: {response.status_code}")
        return embeddings_list
    except Exception as e:
        print("Unable to generate Embeddings response")
        print(f"Exception: {e}")
        return embeddings_list


def gpt_models() -> List:
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
    # mod = gpt_models()
    # print(mod)
    the_text_before = 'Can human nature be changed?'
    the_text_after = 'That is why human nature can not be changed.'
    # # bias the words "Yes" and "No" or the new line "\n".
    # bias = {
    #     # 5297: 1.0,          # Yes
    #     # 2949: -100.0,     # No
    #     # 198: -1.0         # /n
    # }
    # kwa = {
    #     "temperature":      1.0,  # up to 2.0
    #     # "top_p":            0.5,  # up to 1.0
    #     "max_tokens":       256,
    #     "n":                3,
    #     "best_of":          4,
    #     "frequency_penalty": 2.0,
    #     "presence_penalty": 2.0,
    #     # "logprobs":         3,  # up to 5
    #     # "logit_bias":       bias
    #     "stop": ["stop"]
    # }
    #
    # msgs = [
    #     {
    #         "role": "system",
    #         "content": "You are an eloquent assistant. Give concise but substantive answers without introduction and conclusion."
    #     },
    #     {
    #         "role": "user",
    #         "content": the_text_before
    #     }
    # ]
    inp = [the_text_before, the_text_after]
    kwa = {
        "dimensions": 1536
    }
    emb = gpt_embeddings(inp, model='text-embedding-3-large', **kwa) #, model='text-similarity-davinci-001')
    # #
    # # num = count_tokens(prompt1)
    # #
    # # connections = fill_in(text_before=text_before,
    # #                       text_after=text_after,
    # #                       **kwa)
    #
    continuations = gpt_complete(text_before=the_text_before, model='gpt-3.5-turbo-instruct', **kwa)
    # #
    # # answers = answer(messages=msgs, **kwa)
    """
    https://openai.com/blog/gpt-4-api-general-availability
    text-similarity-ada-001
    text-similarity-babbage-001
    text-similarity-curie-001
    text-similarity-davinci-001
    """
    # model = 'text-search-davinci-doc-001' # 'text-search-davinci-doc-001'
    # inp = ["existence"]
    # emb = gpt_embeddings(inp) #, model=model)
    print('ok')