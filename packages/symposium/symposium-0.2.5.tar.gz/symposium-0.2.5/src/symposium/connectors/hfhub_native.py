# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import json
import requests
from os import environ
from huggingface_hub import get_token
from huggingface_hub import InferenceClient


HF_TOKEN = environ.get('HF_TOKEN', '')


API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}
def query(payload):
    response = requests.request("POST",
                                API_URL,
                                headers=headers,
                                json=payload)

    return json.loads(response.content.decode("utf-8"))


if __name__ == "__main__":
    # hf_token = get_token()
    client = InferenceClient("mistralai/Mistral-7B-Instruct-v0.1", token=HF_TOKEN)
    other = client.list_deployed_models()
    resp = client.text_generation(prompt="Hi, I am Alex", max_new_tokens=1000)
    print("ok")