# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from os import environ
from typing import List, Dict
import requests
from ..adapters.plm_rest import prepared_plm_prompt, format_plm_output


palm_key                = environ.get("GOOGLE_API_KEY","") # PALM_KEY", "")
palm_api_base           = environ.get("PALM_API_BASE","https://generativelanguage.googleapis.com/v1beta3")
palm_completion_model   = environ.get("PALM_DEFAULT_TEXT_MODEL", "text-bison-001")
palm_chat_model         = environ.get("PALM_DEFAULT_CHAT_MODEL", "chat-bison-001")
palm_embedding_model    = environ.get("PALM_DEFAULT_EMBEDDING_MODEL", "embedding-gecko-001")


def palm_message(messages,
                 context,
                 examples,
                 **kwargs):

    """A simple requests call to Palm message generation endpoint.
        kwargs:
            temperature     = 0 to 1.0
            top_p           = 0.0 to 1.0
            top_k           = None (number of considered tokens)
            n               = 1 to 8 # number of candidates
            max_tokens      = number of tokens
    """
    responses = []
    json_data = {
        "prompt": {
            "context":  kwargs.get("context", context), # context,
            "examples": kwargs.get("examples", examples), #examples,
            "messages": kwargs.get("messages", messages) #messages
        },
        "temperature": kwargs.get("temperature", 0.5),
        "candidateCount": kwargs.get("n", 1),
        "topP": kwargs.get("top_p", 0.1),
        "topK": kwargs.get("top_k", None)
        }
    try:
        url = f"{palm_api_base}/models/{kwargs.get('model', palm_chat_model)}:generateMessage"
        response = requests.post(
            url=url,
            params=f"key={palm_key}",
            json=json_data,
        )
        if response.status_code == requests.codes.ok:
            for count, candidate in enumerate(response.json()['candidates']):
                item = {"index": count,
                        "author": candidate['author'],
                        "content": candidate['content']}
                responses.append(item)
        else:
            print(f"Request status code: {response.status_code}")
            print(response.json()['content'])
        return responses

    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return responses


def palm_complete(messages=None, recorder=None, **kwargs):
    """A completions endpoint call through requests.
        kwargs:
            temperature     = 0 to 1.0
            top_p           = 0.0 to 1.0
            top_k           = The maximum number of tokens to consider when sampling.
            n               = 1 to 8 # number of candidates
            max_tokens      = number of tokens
            stop            = ["stop"]  array of up to 4 sequences
    """
    record, formatted_prompt = prepared_plm_prompt(
        kwargs.get("messages", messages)
    )
    garbage = [{"category": "HARM_CATEGORY_UNSPECIFIED",    "threshold": "BLOCK_NONE"},  # 0-th category
               {"category": "HARM_CATEGORY_DEROGATORY",     "threshold": "BLOCK_NONE"},
               {"category": "HARM_CATEGORY_TOXICITY",       "threshold": "BLOCK_NONE"},
               {"category": "HARM_CATEGORY_VIOLENCE",       "threshold": "BLOCK_NONE"},
               {"category": "HARM_CATEGORY_SEXUAL",         "threshold": "BLOCK_NONE"},
               {"category": "HARM_CATEGORY_MEDICAL",        "threshold": "BLOCK_NONE"},
               {"category": "HARM_CATEGORY_DANGEROUS",      "threshold": "BLOCK_NONE"},
    ]

    responses = []
    json_data = {"prompt":          formatted_prompt,
                 "temperature":     kwargs.get("temperature", 0.5),
                 "candidateCount":  kwargs.get("n", 1),
                 "safetySettings":  garbage,
                 "maxOutputTokens": kwargs.get("max_tokens", 256),
                 "topP":            kwargs.get("top_p", 0.5),
                 "topK":            kwargs.get("top_k", None)
                }
    try:
        url = f"{palm_api_base}/models/{kwargs.get('model', palm_completion_model)}:generateText"
        response = requests.post(
            url=url,
            params=f"key={palm_key}",
            json=json_data,
        )
        if response.status_code == requests.codes.ok:
            if response.json().get('filters', None):
                raise Exception('Results filtered')
            else:
                response_dump = response.json()
                if recorder:
                    log_message = {"query": json_data, "response": response_dump}
                    recorder.log_event(log_message)
        else:
            print(f"Request status code: {response.status_code}")
            return None
        formatted, other = format_plm_output(response_dump)
        if other:
            formatted['other'] = other
        if recorder:
            rec = {'messages': record, 'response': formatted}
            recorder.record(rec)
            return formatted
    except Exception as e:
        print(f"Unable to generate continuations response, {e}")
        return None


def palm_embeddings(input_list: List[str],
                    model=palm_embedding_model, **kwargs) -> List[Dict]:
    """Returns the embedding of a list of text strings.
    """
    embeddings_list = []
    json_data = {"texts": input_list} | kwargs
    try:
        response = requests.post(
            f"{palm_api_base}/models/{kwargs.get('model', palm_embedding_model)}:batchEmbedText",
            params=f"key={palm_key}",
            json=json_data,
        )
        if response.status_code == requests.codes.ok:
            # embeddings_list = response.json()['embeddings']
            for count, candidate in enumerate(response.json()['embeddings']):
                item = {"index": count, "embedding": candidate['value']}
                embeddings_list.append(item)
        else:
            print(f"Request status code: {response.status_code}")
        return embeddings_list
    except Exception as e:
        print("Unable to generate Embeddings response")
        print(f"Exception: {e}")
        return embeddings_list


if __name__ == '__main__':
    print('you called main')
