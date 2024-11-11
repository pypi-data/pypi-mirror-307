# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import json
import requests
from os import environ


HF_TOKEN = environ.get('HUGGINGFACE_TOKEN', '')


API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}
def query(payload):
    response = requests.request("POST",
                                API_URL,
                                headers=headers,
                                json=payload)

    return json.loads(response.content.decode("utf-8"))


if __name__ == "__main__":
    json_data = "Can you please let us know more details about your "
    # data = query("Can you please let us know more details about your ")
    result = query(json_data)
    print("ok")