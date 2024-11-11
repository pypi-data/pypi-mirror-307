# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from ..util.xml_tags import extract_xml_tagged_content


def prepared_coh_messages(input):
    """
    :input_format
        messages = [
            {"role": "world",   "name": "cohere",   "content": "Be an Abstract Intellect."},
            {"role": "human",   "name": "alex",     "content": "Can we discuss this?"},
            {"role": "machine", "name": "coral",   "content": "Yes."}
            {"role": "human",   "name": "alex",     "content": "Then let's do it."}
        ]
    :outputformat
        messages = [
            {"role": "SYSTEM",      "content": "Be an Abstract Intellect."}
            {"role": "USER",        "content": "Can we discuss this?"}
            {"role": "CHATBOT",     "content": "Yes."}
            {"role": "USER",        "content": "Then let's do it."}
        ]
    """
    output_messages = []
    for message in input:
        output_message = {}
        if message['role'] == 'human':
            output_message['role'] = 'USER'
        elif message['role'] == 'machine':
            output_message['role'] = 'CHATBOT'
        elif message['role'] == 'world':
            output_message['role'] = 'SYSTEM'
        output_message['message'] = message['content']
        output_messages.append(output_message)
    return input, output_messages


def formatted_coh_message(output):
    """
    :input_format
        messages = [
            {"role": "assistant",   "content": "I will lay it out later"}
        ]
    :outputformat
        messages = [
            {"role": "machine", "name": "chatgpt",   "content": "I will lay it out later"}
        ]
    """
    formatted_output = {}
    last_message = output['chat_history'][-1]
    if output['role'] == 'CHATBOT':
        formatted_output['role'] = 'machine'
        formatted_output['name'] = 'coral'
        # txt, tags = extract_xml_tagged_content(
        #     output['content'],
        #     placeholders=True # default for now delete if not needed.
        # )
        formatted_output['content'] = last_message['message']
        # if len(tags) > 0:
        #     formatted_output['tags'] = tags
    else:
        print('The role is not assistant')
    return formatted_output


def format_coh_output(output):
    """
    :list of choices
    :return: formatted_output, other
    """
    solo_candidate = output['choices'].pop(0)
    formatted_output = formatted_coh_message(solo_candidate['message'])
    if len(output['choices']) > 0:
        other = []
        for choice in output['choices']:
            other_formatted = formatted_coh_message(choice['message'])
            other.append(other_formatted)
    else:
        other = None
    return formatted_output, other
