# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from os import environ
from typing import List, Dict
import requests
from ..adapters.gem_rest import prepared_gem_messages, formatted_gem_output


gemini_key              = environ.get("GOOGLE_API_KEY","") # GEMINI_KEY", "")
gemini_api_base         = environ.get("GEMINI_API_BASE","https://generativelanguage.googleapis.com/v1beta")
gemini_content_model    = environ.get("GEMINI_DEFAULT_CONTENT_MODEL", "gemini-1.0-pro")
gemini_embedding_model  = environ.get("GEMINI_DEFAULT_EMBEDDING_MODEL", "embedding-001")

garbage = [
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT","threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH","threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HARASSMENT","threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT","threshold": "BLOCK_NONE"}
]


def gemini_message(messages: List,
                   recorder=None,
                   **kwargs):

    """A completions endpoint call through requests.
        kwargs:
            temperature     = 0 to 1.0
            top_p           = 0.0 to 1.0
            top_k           = The maximum number of tokens to consider when sampling.
            n               = 1 mandatory
            max_tokens      = number of tokens
            stop            = ["stop"]  array of up to 4 sequences
    """
    record, formatted_messages = prepared_gem_messages(kwargs.get("messages", messages))
    json_data = {
                 "contents":            formatted_messages,
                 "safetySettings":      garbage,
                 "generationConfig":{
                     "stopSequences":   kwargs.get("stop_sequences", ["STOP","Title"]),
                     "temperature":     kwargs.get("temperature", 0.5),
                     "maxOutputTokens": kwargs.get("max_tokens", 100),
                     "candidateCount":  kwargs.get("n", 1),  # mandatory 1
                     "topP":            kwargs.get("top_p", 0.9),
                     "topK":            kwargs.get("top_k", None)
                 }
            }
    try:
        response = requests.post(
            url=f"{gemini_api_base}/models/{kwargs.get('model', gemini_content_model)}:generateContent",
            params=f"key={gemini_key}",
            json=json_data,
        )
        if response.status_code == requests.codes.ok:
            if response.json().get('filters', None):
                raise Exception('Results filtered')
            else:
                msg_dump = response.json()
                if recorder:
                    log_message = {"query": json_data, "response": msg_dump}
                    recorder.log_event(log_message)
        else:
            print(f"Request status code: {response.status_code}")
            return None
        formatted = formatted_gem_output(msg_dump)
        if recorder:
            rec = {'messages': record,'response': formatted}
            recorder.record(rec)
            return formatted
    except Exception as e:
        print(f"Unable to generate continuations response, {e}")
        return None


def gemini_answer(contents: List,
                  recorder=None,
                  **kwargs):

    """A completions endpoint call through requests.
        kwargs:
            temperature     = 0 to 1.0
            top_p           = 0.0 to 1.0
            top_k           = The maximum number of tokens to consider when sampling.
            n               = 1 mandatory
            max_tokens      = number of tokens
            stop            = ["stop"]  array of up to 4 sequences
    """
    # answerStyle =
    # ANSWER_STYLE_UNSPECIFIED = 0,
    # ABSTRACTIVE	Succint but abstract style
    # EXTRACTIVE	Very brief and extractive style.
    # VERBOSE       Verbose style including extra details. The response may be formatted as a sentence,
    #               paragraph, multiple paragraphs, or bullet points, etc.
    json_data = {"contents": contents,
                 "answerStyle": 1,
                 "safetySettings":  garbage,
                 "temperature":     kwargs.get("temperature", 0.5)
            }
    try:

        response = requests.post(
            url=f"{gemini_api_base}/models/{kwargs.get('model', gemini_content_model)}:generateAnswer",
            params=f"key={gemini_key}",
            json=json_data,
        )
        if response.status_code == requests.codes.ok:
            if response.json().get('filters', None):
                raise Exception('Results filtered')
            else:
                answer_dump = response.json()
                if recorder:
                    log_message = {"query": json_data, "response": answer_dump}
                    recorder.log_event(log_message)
        else:
            print(f"Request status code: {response.status_code}")
            return None
        if recorder:
            rec = {'messages': json_data['contents'], 'response': answer_dump['candidates']}
            recorder.record(rec)
    except Exception as e:
        print(f"Unable to generate continuations response, {e}")
        return None


def gemini_embeddings(input_list: List[str],
                      **kwargs) -> List[Dict]:
    """Returns the embedding of a list of text strings.
    """
    embeddings_list = []
    json_data = {"texts": input_list} | kwargs
    try:
        response = requests.post(
            f"{gemini_api_base}/models/{kwargs.get('model', gemini_embedding_model)}:batchEmbedText",
            params=f"key={gemini_key}",
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
        print('you launched main.')
