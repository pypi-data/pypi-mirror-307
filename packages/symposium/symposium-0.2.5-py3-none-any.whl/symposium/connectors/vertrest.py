# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from os import environ
import subprocess
import requests
from typing import List, Dict


vertex_completion_model_id  = environ.get('GCLOUD_COMPLETION_MODEL_ID', 'text-bison')
vertex_chat_model_id        = environ.get('GCLOUD_CHAT_MODEL_ID', 'chat-bison')
vertex_embedding_model_id   = environ.get('GCLOUD_EMBEDDING_MODEL_ID', 'embedding-gecko')
project_id                  = environ.get('GCLOUD_PROJECT_ID', 'ai-dialogue-facilitator')
username                    = environ.get('USERNAME')

token = subprocess.run([f'/home/{username}/google-cloud-sdk/bin/gcloud',
                        'auth',
                        'print-access-token'],
                       stdout=subprocess.PIPE).stdout.decode('utf-8').strip()


def vertex_continuations(text_before,
                         model=vertex_completion_model_id,
                         **kwargs) -> List:
    """A completions endpoint call through requests.
        kwargs:
            temperature     = 0 to 1.0
            top_p           = 0.0 to 1.0
            top_k           = The maximum number of tokens to consider when sampling.
            n               = 1 to 8 # number of candidates
            max_tokens      = number of tokens
            stop            = ["stop"]  array of up to 4 sequences
    """
    responses = []
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
    }
    json_data = {"instances": [{"prompt": text_before}],
                 "parameters": {
                     "temperature":     kwargs.get("temperature", 0.5),
                     "candidateCount":  kwargs.get("n", 1),
                     "maxOutputTokens": kwargs.get("max_tokens", 100),
                     "stopSequences":   kwargs.get('stop_sequences', []),
                     "topP":            kwargs.get("top_p", 0.1),
                     "topK":            kwargs.get("top_k", None)
                 }
            }
    try:
        response = requests.post(
            url = f'https://us-central1-aiplatform.googleapis.com/v1/projects/' \
                  f'{project_id}/locations/us-central1/publishers/google/models/' \
                  f'{model}:predict',
            headers=headers,
            json=json_data,
        )
        if response.status_code == requests.codes.ok:
            res = response.json()
            for count, candidate in enumerate(response.json()['predictions']):
                item = {"index": count,
                        "text": candidate['content'],
                        "finish_reason": 'blocked' if candidate['safetyAttributes']['blocked'] else 'stop'}
                responses.append(item)
        else:
            print(f"Request status code: {response.status_code}")
        return responses

    except Exception as e:
        print(f"Unable to generate continuations response, {e}")
        return responses


def vertex_answer(context: str,
                  examples: List,
                  messages: List,
                  model=vertex_chat_model_id,
                  **kwargs) -> List:
    """A completions endpoint call through requests.
        kwargs:
            temperature     = 0 to 1.0
            top_p           = 0.0 to 1.0
            top_k           = The maximum number of tokens to consider when sampling.
            n               = 1 to 8 # number of candidates
            max_tokens      = number of tokens
            stop            = ["stop"]  array of up to 4 sequences
    """
    responses = []
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
    }
    json_data = {"instances": [{
                    "context": context,
                    "examples": examples,
                    "messages": messages
                 }],
                 "parameters": {
                     "temperature":     kwargs.get("temperature", 0.5),
                     # "candidateCount":  kwargs.get("n", 1),
                     "maxOutputTokens": kwargs.get("max_tokens", 100),
                     # "stopSequences":   kwargs.get('stop_sequences', []),
                     "topP":            kwargs.get("top_p", 0.1),
                     "topK":            kwargs.get("top_k", None)
                 }
            }
    try:
        response = requests.post(
            url = f'https://us-central1-aiplatform.googleapis.com/v1/projects/' \
                  f'{project_id}/locations/us-central1/publishers/google/models/' \
                  f'{model}:predict',
            headers=headers,
            json=json_data,
        )
        if response.status_code == requests.codes.ok:
            res = response.json()
            for count, candidate in enumerate(response.json()['predictions']):
                item = {"index": count,
                        "text": candidate['content'],
                        "finish_reason": 'blocked' if candidate['safetyAttributes']['blocked'] else 'stop'}
                responses.append(item)
        else:
            print(f"Request status code: {response.status_code}")
        return responses

    except Exception as e:
        print(f"Unable to generate continuations response, {e}")
        return responses


if __name__ == "__main__":
    # kwa = {
    #         "temperature": 0.5,
    #         "max_tokens": 10,
    #         "top_k": 20,
    #         "top_p": 0.9,
    #         "stop_sequences": ['stop'],
    #         "n": 2
    # }
    # text = "Can human nature be changed?"
    # responses = vertex_continuations(text_before=text,
    #                                  model=vertex_completion_model_id,
    #                                  **kwa)

    context = "Answer the following question"
    examples = []
    messages = [
        {
            "author": "human",
            "content": "Can human nature be changed?"
        }
    ]
    kwar = {
        "temperature": 0.5,
        "max_tokens": 100,
        "top_k": 20,
        "top_p": 0.9,
    }

    response = vertex_answer(context=context,
                             examples=examples,
                             messages=messages,
                             model="chat-bison@002",
                             **kwar)

    print("ok")